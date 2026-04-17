/**
 * PDF Data Processor
 * Handles reading and extracting data from PDF files
 */

const pdfParse = require('pdf-parse');
const logger = require('../utils/logger');
const fs = require('fs').promises;
const path = require('path');

class PDFProcessor {
  constructor(config = {}) {
    this.chunkSize = config.chunkSize || 1500;
    this.chunkOverlap = config.chunkOverlap || 300;
  }

  /**
   * Read PDF file and extract text
   */
  async readPDF(filePath) {
    try {
      logger.info(`Reading PDF file: ${filePath}`);
      
      if (!await this.fileExists(filePath)) {
        throw new Error(`File not found: ${filePath}`);
      }

      const dataBuffer = await fs.readFile(filePath);
      const data = await pdfParse(dataBuffer);

      const result = {
        text: data.text,
        pages: data.numpages,
        info: data.info,
        metadata: {
          author: data.info?.Author,
          title: data.info?.Title,
          subject: data.info?.Subject,
          creator: data.info?.Creator
        }
      };

      logger.info(`PDF file processed successfully`, {
        pages: result.pages,
        textLength: result.text.length
      });

      return result;
    } catch (error) {
      logger.error('Error reading PDF file', { error: error.message });
      throw error;
    }
  }

  /**
   * Convert PDF text to chunks for RAG
   */
  async convertToChunks(pdfData, fileName) {
    try {
      const chunks = [];
      const text = pdfData.text;
      
      // Split by pages (assuming page markers exist)
      const pageTexts = this.splitIntoPages(text);
      
      let chunkIndex = 0;
      let currentPage = 1;
      let currentChunk = '';

      for (const pageText of pageTexts) {
        const paragraphs = pageText.split(/\n\n+/);
        
        for (const paragraph of paragraphs) {
          if ((currentChunk + paragraph).length > this.chunkSize) {
            if (currentChunk) {
              chunks.push({
                id: `${fileName}-page-${currentPage}-chunk-${chunkIndex}`,
                source: fileName,
                content: currentChunk.trim(),
                metadata: {
                  type: 'pdf',
                  page: currentPage,
                  chunkIndex,
                  length: currentChunk.length,
                  ...pdfData.metadata
                }
              });
              chunkIndex++;
              
              // Create overlap
              const sentences = currentChunk.split('. ');
              const overlapSentences = sentences.slice(-2);
              currentChunk = overlapSentences.join('. ') + '. ' + paragraph;
            } else {
              currentChunk = paragraph;
            }
          } else {
            currentChunk += (currentChunk ? '\n\n' : '') + paragraph;
          }
        }
        
        currentPage++;
        chunkIndex = 0; // Reset chunk index for each page
      }

      // Add final chunk
      if (currentChunk) {
        chunks.push({
          id: `${fileName}-page-${currentPage}-chunk-${chunkIndex}`,
          source: fileName,
          content: currentChunk.trim(),
          metadata: {
            type: 'pdf',
            page: currentPage,
            chunkIndex,
            length: currentChunk.length,
            ...pdfData.metadata
          }
        });
      }

      logger.info(`Created ${chunks.length} text chunks from PDF`);
      return chunks;
    } catch (error) {
      logger.error('Error converting PDF to chunks', { error: error.message });
      throw error;
    }
  }

  /**
   * Split text into pages
   */
  splitIntoPages(text) {
    // Try to detect page boundaries
    const pageBreaks = text.split(/\f/); // Form feed character
    
    if (pageBreaks.length > 1) {
      return pageBreaks;
    }
    
    // If no page breaks, split by approximate page length
    const avgCharsPerPage = 3000;
    const pages = [];
    
    for (let i = 0; i < text.length; i += avgCharsPerPage) {
      pages.push(text.slice(i, i + avgCharsPerPage));
    }
    
    return pages;
  }

  /**
   * Extract structured data from PDF
   */
  extractStructuredData(text) {
    const structuredData = {
      headings: [],
      tables: [],
      keyPoints: []
    };

    // Extract headings (lines in ALL CAPS or ending with :)
    const lines = text.split('\n');
    structuredData.headings = lines.filter(line => 
      line.trim() && 
      (line === line.toUpperCase() || line.trim().endsWith(':'))
    );

    // Extract key points (lines starting with bullets or numbers)
    structuredData.keyPoints = lines.filter(line =>
      line.trim().match(/^[\*\-\•]\d*\./) || 
      line.trim().match(/^\d+\./)
    );

    return structuredData;
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
   * Process PDF file and return chunks ready for RAG
   */
  async process(filePath) {
    const pdfData = await this.readPDF(filePath);
    const chunks = await this.convertToChunks(pdfData, path.basename(filePath));
    
    const structuredData = this.extractStructuredData(pdfData.text);
    
    return {
      source: path.basename(filePath),
      type: 'pdf',
      chunks,
      structuredData,
      metadata: {
        pages: pdfData.pages,
        totalChunks: chunks.length,
        ...pdfData.metadata
      }
    };
  }
}

module.exports = PDFProcessor;
