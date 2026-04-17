/**
 * Connection Test Utility
 * Tests API connections and system configuration
 */

const logger = require('./logger');
const GeminiApiClient = require('../llm/GeminiApiClient');
const config = require('../../config/config.json');

async function testGeminiConnection() {
  try {
    logger.info('Testing Gemini API connection...');
    
    const client = new GeminiApiClient(config.gemini);
    const isConnected = await client.testConnection();
    
    if (isConnected) {
      logger.info('✅ Gemini API connection successful');
      return true;
    } else {
      logger.error('❌ Gemini API connection failed');
      return false;
    }
  } catch (error) {
    logger.error('❌ Gemini API test error', { error: error.message });
    return false;
  }
}

async function testFileSystem() {
  try {
    logger.info('Testing file system access...');
    
    const fs = require('fs').promises;
    const path = require('path');
    
    // Test directories
    const dirs = [
      'data/input/excel',
      'data/input/pdf',
      'data/output/rag',
      'data/vectorstore'
    ];
    
    for (const dir of dirs) {
      try {
        await fs.access(dir);
        logger.info(`✅ Directory accessible: ${dir}`);
      } catch {
        logger.warn(`⚠️  Directory not found: ${dir}`);
        await fs.mkdir(dir, { recursive: true });
        logger.info(`✅ Directory created: ${dir}`);
      }
    }
    
    return true;
  } catch (error) {
    logger.error('❌ File system test failed', { error: error.message });
    return false;
  }
}

async function testConfiguration() {
  try {
    logger.info('Testing configuration...');
    
    if (!config.gemini.apiKey || config.gemini.apiKey === 'YOUR_GEMINI_API_KEY') {
      logger.warn('⚠️  Gemini API key not configured');
      return false;
    }
    
    logger.info('✅ Configuration loaded successfully');
    logger.info('Configuration details:', {
      geminiModel: config.gemini.model,
      embeddingModel: config.rag.embeddingModel,
      maxDocuments: config.rag.maxDocuments
    });
    
    return true;
  } catch (error) {
    logger.error('❌ Configuration test failed', { error: error.message });
    return false;
  }
}

async function runAllTests() {
  logger.info('🧪 Starting Data Scooper connection tests...\n');
  
  const results = {
    configuration: await testConfiguration(),
    fileSystem: await testFileSystem(),
    geminiApi: await testGeminiConnection()
  };
  
  console.log('\n📊 Test Results Summary:');
  console.log('='.repeat(50));
  console.log(`Configuration: ${results.configuration ? '✅ PASS' : '❌ FAIL'}`);
  console.log(`File System:  ${results.fileSystem ? '✅ PASS' : '❌ FAIL'}`);
  console.log(`Gemini API:  ${results.geminiApi ? '✅ PASS' : '❌ FAIL'}`);
  console.log('='.repeat(50));
  
  const allPassed = Object.values(results).every(result => result === true);
  
  if (allPassed) {
    logger.info('🎉 All tests passed! System is ready to use.');
    process.exit(0);
  } else {
    logger.error('⚠️  Some tests failed. Please check the configuration.');
    process.exit(1);
  }
}

// Run tests if executed directly
if (require.main === module) {
  runAllTests().catch(error => {
    logger.error('Test execution failed', { error: error.message });
    process.exit(1);
  });
}

module.exports = {
  testGeminiConnection,
  testFileSystem,
  testConfiguration,
  runAllTests
};
