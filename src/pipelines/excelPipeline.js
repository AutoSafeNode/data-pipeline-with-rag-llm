/**
 * Excel to RAG Pipeline
 * Processes Excel files and converts them to RAG-ready format
 */

const logger = require('../utils/logger');
const ExcelProcessor = require('../processors/excelProcessor');
const TextProcessor = require('../processors/textProcessor');
const EmbeddingGenerator = require('../rag/embeddings');
const VectorStore = require('../rag/vectorStore');
const fs = require('fs').promises;
const path = require('path');

class ExcelToRAGPipeline {
  constructor(config) {
    this.config = config;
    this.excelProcessor = new ExcelProcessor(config);
    this.textProcessor = new TextProcessor(config);
    this.embeddingGenerator = new EmbeddingGenerator(config);
    this.vectorStore = new VectorStore(config);
  }

  /**
   * Process single Excel file
   */
  async processFile(filePath) {
    try {
      logger.info(`Processing Excel file: ${filePath}`);

      // Step 1: Read and extract data from Excel
      const excelData = await this.excelProcessor.readExcel(filePath);
      
      // Step 2: Convert to chunks
      const chunks = await this.excelProcessor.convertToChunks(excelData);
      
      // Step 3: Process and validate chunks
      const processedChunks = this.textProcessor.processChunks(chunks);
      
      // Step 4: Generate embeddings for chunks
      const chunksWithEmbeddings = await this.embeddingGenerator.generateEmbeddings(processedChunks);
      
      // Step 5: Store in vector store
      const storeResult = await this.vectorStore.store(chunksWithEmbeddings);

      logger.info(`Excel file processed successfully`, {
        fileName: path.basename(filePath),
        totalChunks: processedChunks.length,
        storeResult
      });

      return {
        success: true,
        fileName: path.basename(filePath),
        chunks: processedChunks.length,
        embeddings: chunksWithEmbeddings.length,
        vectorStoreId: storeResult.id
      };
    } catch (error) {
      logger.error(`Error processing Excel file: ${filePath}`, { 
        error: error.message 
      });
      throw error;
    }
  }

  /**
   * Process all Excel files in directory
   */
  async processDirectory(inputDir) {
    try {
      logger.info(`Processing Excel files from directory: ${inputDir}`);

      const files = await fs.readdir(inputDir);
      const excelFiles = files.filter(file => 
        file.endsWith('.xlsx') || 
        file.endsWith('.xls') ||
        file.endsWith('.xlsm')
      );

      if (excelFiles.length === 0) {
        logger.warn('No Excel files found in directory');
        return { processed: 0, results: [] };
      }

      logger.info(`Found ${excelFiles.length} Excel files to process`);

      const results = [];
      for (const file of excelFiles) {
        const filePath = path.join(inputDir, file);
        
        try {
          const result = await this.processFile(filePath);
          results.push(result);
        } catch (error) {
          logger.error(`Failed to process ${file}`, { error: error.message });
          results.push({
            success: false,
            fileName: file,
            error: error.message
          });
        }
      }

      const successful = results.filter(r => r.success).length;
      
      logger.info(`Directory processing complete`, {
        total: excelFiles.length,
        successful,
        failed: excelFiles.length - successful
      });

      return {
        processed: excelFiles.length,
        successful,
        failed: excelFiles.length - successful,
        results
      };
    } catch (error) {
      logger.error('Error processing directory', { error: error.message });
      throw error;
    }
  }

  /**
   * Save processed data to file
   */
  async saveToFile(data, outputPath) {
    try {
      const outputDir = path.dirname(outputPath);
      await fs.mkdir(outputDir, { recursive: true });

      const jsonData = JSON.stringify(data, null, 2);
      await fs.writeFile(outputPath, jsonData, 'utf8');

      logger.info(`Data saved to ${outputPath}`);
      return outputPath;
    } catch (error) {
      logger.error('Error saving data to file', { error: error.message });
      throw error;
    }
  }

  /**
   * Main execution method
   */
  async run(inputPath) {
    try {
      const stats = await fs.stat(inputPath);
      
      let result;
      if (stats.isDirectory()) {
        result = await this.processDirectory(inputPath);
      } else {
        result = await this.processFile(inputPath);
      }

      // Save results
      const timestamp = new Date().toISOString().replace(/:/g, '-');
      const outputPath = path.join(
        this.config.outputDir,
        `excel-rag-${timestamp}.json`
      );
      await this.saveToFile(result, outputPath);

      return result;
    } catch (error) {
      logger.error('Pipeline execution failed', { error: error.message });
      throw error;
    }
  }
}

// Main execution
if (require.main === module) {
  const config = require('../../config/config.json').pipelines.excel;
  const pipeline = new ExcelToRAGPipeline(config);
  
  const inputPath = process.argv[2] || config.inputDir;
  
  pipeline.run(inputPath)
    .then(() => {
      logger.info('Excel pipeline completed successfully');
      process.exit(0);
    })
    .catch((error) => {
      logger.error('Excel pipeline failed', { error: error.message });
      process.exit(1);
    });
}

module.exports = ExcelToRAGPipeline;
