/**
 * Data Scooper - Main Entry Point
 * Data pipeline for converting Excel/PDF to RAG and LLM integration
 */

const logger = require('./utils/logger');
const ExcelToRAGPipeline = require('./pipelines/excelPipeline');
const PDFToRAGPipeline = require('./pipelines/pdfPipeline');
const GeminiApiClient = require('./llm/GeminiApiClient');
const config = require('../config/config.json');

class DataScooper {
  constructor(config) {
    this.config = config;
  }

  /**
   * Process Excel files to RAG
   */
  async processExcel(inputPath) {
    try {
      logger.info('Starting Excel to RAG pipeline');
      const pipeline = new ExcelToRAGPipeline(config.pipelines.excel);
      const result = await pipeline.run(inputPath);
      logger.info('Excel pipeline completed', { result });
      return result;
    } catch (error) {
      logger.error('Excel pipeline failed', { error: error.message });
      throw error;
    }
  }

  /**
   * Process PDF files to RAG
   */
  async processPDF(inputPath) {
    try {
      logger.info('Starting PDF to RAG pipeline');
      const pipeline = new PDFToRAGPipeline(config.pipelines.pdf);
      const result = await pipeline.run(inputPath);
      logger.info('PDF pipeline completed', { result });
      return result;
    } catch (error) {
      logger.error('PDF pipeline failed', { error: error.message });
      throw error;
    }
  }

  /**
   * Query LLM with RAG context
   */
  async queryWithRAG(query, ragData) {
    try {
      logger.info('Querying LLM with RAG context');
      const client = new GeminiApiClient(config.gemini);
      
      const apiRequest = {
        systemInstruction: {
          parts: [{ text: 'You are a helpful assistant that answers questions based on the provided context.' }]
        },
        contents: [
          { parts: [{ text: `Context: ${JSON.stringify(ragData)}\n\nQuestion: ${query}` }] }
        ]
      };

      const response = await client.generateContent(apiRequest);
      logger.info('LLM query completed');
      return response;
    } catch (error) {
      logger.error('LLM query failed', { error: error.message });
      throw error;
    }
  }

  /**
   * Run complete pipeline
   */
  async runCompletePipeline(excelPath, pdfPath) {
    try {
      logger.info('Starting complete data pipeline');

      const results = {};

      if (excelPath) {
        results.excel = await this.processExcel(excelPath);
      }

      if (pdfPath) {
        results.pdf = await this.processPDF(pdfPath);
      }

      logger.info('Complete pipeline finished', { results });
      return results;
    } catch (error) {
      logger.error('Complete pipeline failed', { error: error.message });
      throw error;
    }
  }
}

// CLI execution
if (require.main === module) {
  const args = process.argv.slice(2);
  const command = args[0];
  const inputPath = args[1];

  const scooper = new DataScooper(config);

  switch (command) {
    case 'excel':
      scooper.processExcel(inputPath)
        .then(() => process.exit(0))
        .catch(() => process.exit(1));
      break;

    case 'pdf':
      scooper.processPDF(inputPath)
        .then(() => process.exit(0))
        .catch(() => process.exit(1));
      break;

    case 'all':
      const excelInput = args[1];
      const pdfInput = args[2];
      scooper.runCompletePipeline(excelInput, pdfInput)
        .then(() => process.exit(0))
        .catch(() => process.exit(1));
      break;

    default:
      console.log(`
Usage: node src/index.js <command> [options]

Commands:
  excel <path>    Process Excel files to RAG
  pdf <path>      Process PDF files to RAG
  all <excel> <pdf>  Process both Excel and PDF files

Examples:
  node src/index.js excel ./data/input/excel
  node src/index.js pdf ./data/input/pdf
  node src/index.js all ./data/input/excel ./data/input/pdf
      `);
      process.exit(1);
  }
}

module.exports = DataScooper;
