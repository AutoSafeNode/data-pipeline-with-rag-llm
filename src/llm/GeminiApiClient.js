/**
 * Gemini API Client
 * 
 * This module handles communication with the Google Gemini API
 * for generating stock analysis reports.
 */

const { GoogleGenerativeAI } = require('@google/generative-ai');
const logger = require('../utils/logger');

class GeminiApiClient {
  constructor(config) {
    if (!config.apiKey) {
      throw new Error('Gemini API key is required');
    }
    
    this.genAI = new GoogleGenerativeAI(config.apiKey);
    this.modelName = config.model || 'gemini-pro';
    this.generationConfig = {
      temperature: 0.3,  // Lower temperature for more consistent financial analysis
      topK: 40,
      topP: 0.95,
      maxOutputTokens: 2048,
    };
  }

  /**
   * Generates content using the Gemini API
   * @param {Object} apiRequest - Formatted API request
   * @returns {Promise<string>} Generated analysis text
   */
  async generateContent(apiRequest) {
    try {
      logger.info('Sending request to Gemini API');
      
      // Get the model
      const model = this.genAI.getGenerativeModel({ 
        model: this.modelName,
        generationConfig: this.generationConfig
      });
      
      // Create the chat session with system instruction
      const chat = model.startChat({
        history: [
          {
            role: "user",
            parts: [{ text: apiRequest.systemInstruction.parts[0].text }]
          },
          {
            role: "model",
            parts: [{ text: "이해했습니다. 글로벌 투자 은행의 선임 주식 분석가로서 제공된 재무 지표를 기반으로 객관적인 가치 평가와 투자 관점을 제시하겠습니다." }]
          }
        ]
      });
      
      // Send the user query
      const result = await chat.sendMessage(apiRequest.contents[0].parts[0].text);
      const response = await result.response;
      const text = response.text();
      
      logger.info('Received response from Gemini API', { 
        responseLength: text.length 
      });
      
      return text;
      
    } catch (error) {
      logger.error('Gemini API request failed', { 
        error: error.message,
        stack: error.stack 
      });
      
      throw new Error(`Gemini API Error: ${error.message}`);
    }
  }

  /**
   * Alternative method for simple text generation
   * @param {string} prompt - The prompt to send
   * @returns {Promise<string>} Generated text
   */
  async generateSimpleContent(prompt) {
    try {
      const model = this.genAI.getGenerativeModel({ 
        model: this.modelName,
        generationConfig: this.generationConfig
      });
      
      const result = await model.generateContent(prompt);
      const response = await result.response;
      const text = response.text();
      
      return text;
      
    } catch (error) {
      logger.error('Simple content generation failed', { 
        error: error.message 
      });
      
      throw new Error(`Gemini API Error: ${error.message}`);
    }
  }

  /**
   * Tests the API connection
   * @returns {Promise<boolean>} True if connection is successful
   */
  async testConnection() {
    try {
      const testPrompt = "테스트 메시지입니다. '연결 성공'이라고 답변해주세요.";
      const response = await this.generateSimpleContent(testPrompt);
      
      const isConnected = response.includes('연결 성공');
      
      logger.info('API connection test completed', { 
        success: isConnected 
      });
      
      return isConnected;
      
    } catch (error) {
      logger.error('API connection test failed', { 
        error: error.message 
      });
      
      return false;
    }
  }
}

module.exports = GeminiApiClient;