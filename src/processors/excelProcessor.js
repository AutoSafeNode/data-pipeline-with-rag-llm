/**
 * Excel Data Processor
 * Handles reading and extracting data from Excel files
 */

const XLSX = require('xlsx');
const logger = require('../utils/logger');
const fs = require('fs').promises;
const path = require('path');

class ExcelProcessor {
  constructor(config = {}) {
    this.chunkSize = config.chunkSize || 1000;
    this.chunkOverlap = config.chunkOverlap || 200;
  }

  /**
   * Read Excel file and extract data
   */
  async readExcel(filePath) {
    try {
      logger.info(`Reading Excel file: ${filePath}`);
      
      if (!await this.fileExists(filePath)) {
        throw new Error(`File not found: ${filePath}`);
      }

      const workbook = XLSX.readFile(filePath);
      const result = [];

      // Iterate through all sheets
      workbook.SheetNames.forEach(sheetName => {
        const worksheet = workbook.Sheets[sheetName];
        const data = XLSX.utils.sheet_to_json(worksheet, { header: 1 });
        
        result.push({
          sheetName,
          data: this.cleanData(data),
          rowCount: data.length,
          columnCount: data[0]?.length || 0
        });
      });

      logger.info(`Excel file processed successfully`, {
        sheets: result.length,
        totalRows: result.reduce((sum, sheet) => sum + sheet.rowCount, 0)
      });

      return result;
    } catch (error) {
      logger.error('Error reading Excel file', { error: error.message });
      throw error;
    }
  }

  /**
   * Convert Excel data to text chunks for RAG
   */
  async convertToChunks(excelData) {
    try {
      const chunks = [];

      for (const sheet of excelData) {
        const sheetText = this.sheetToText(sheet);
        const sheetChunks = this.textToChunks(sheetText, sheet.sheetName);
        chunks.push(...sheetChunks);
      }

      logger.info(`Created ${chunks.length} text chunks from Excel data`);
      return chunks;
    } catch (error) {
      logger.error('Error converting Excel to chunks', { error: error.message });
      throw error;
    }
  }

  /**
   * Convert sheet data to formatted text
   */
  sheetToText(sheet) {
    let text = `Sheet: ${sheet.sheetName}\n\n`;
    
    sheet.data.forEach((row, rowIndex) => {
      if (rowIndex === 0) {
        // Header row
        text += `Headers: ${row.join(' | ')}\n`;
        text += '=' .repeat(80) + '\n';
      } else {
        // Data rows
        const rowData = row.map((cell, cellIndex) => {
          const header = sheet.data[0][cellIndex] || `Column${cellIndex}`;
          return `${header}: ${cell}`;
        }).join(', ');
        text += `Row ${rowIndex}: ${rowData}\n`;
      }
    });

    return text;
  }

  /**
   * Split text into chunks with overlap
   */
  textToChunks(text, source) {
    const chunks = [];
    const sentences = text.split(/\n\n+/);
    
    let currentChunk = '';
    let chunkIndex = 0;

    for (const sentence of sentences) {
      if ((currentChunk + sentence).length > this.chunkSize) {
        if (currentChunk) {
          chunks.push({
            id: `${source}-chunk-${chunkIndex}`,
            source,
            content: currentChunk.trim(),
            metadata: {
              type: 'excel',
              chunkIndex,
              length: currentChunk.length
            }
          });
          chunkIndex++;
          
          // Create overlap
          const words = currentChunk.split(' ');
          const overlapWords = words.slice(-Math.floor(this.chunkOverlap / 10));
          currentChunk = overlapWords.join(' ') + '\n\n' + sentence;
        } else {
          currentChunk = sentence;
        }
      } else {
        currentChunk += (currentChunk ? '\n\n' : '') + sentence;
      }
    }

    // Add final chunk
    if (currentChunk) {
      chunks.push({
        id: `${source}-chunk-${chunkIndex}`,
        source,
        content: currentChunk.trim(),
        metadata: {
          type: 'excel',
          chunkIndex,
          length: currentChunk.length
        }
      });
    }

    return chunks;
  }

  /**
   * Clean and validate data
   */
  cleanData(data) {
    return data.filter(row => row && row.length > 0);
  }

  /**
   * Check if file exists
   */
  async fileExists(filePath) {
    try {
      await fs.access(filePath);
      return true;
    } catch {
      return false;
    }
  }

  /**
   * Process Excel file and return chunks ready for RAG
   */
  async process(filePath) {
    const excelData = await this.readExcel(filePath);
    const chunks = await this.convertToChunks(excelData);
    
    return {
      source: path.basename(filePath),
      type: 'excel',
      chunks,
      metadata: {
        sheets: excelData.length,
        totalChunks: chunks.length
      }
    };
  }
}

module.exports = ExcelProcessor;
