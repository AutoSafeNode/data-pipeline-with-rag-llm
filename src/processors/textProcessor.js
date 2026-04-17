/**
 * Text Processor
 * Handles text processing and normalization for RAG
 */

const logger = require('../utils/logger');

class TextProcessor {
  constructor(config = {}) {
    this.minChunkSize = config.minChunkSize || 100;
    this.maxChunkSize = config.maxChunkSize || 2000;
  }

  /**
   * Normalize text content
   */
  normalizeText(text) {
    if (!text) return '';
    
    return text
      .replace(/\s+/g, ' ')           // Multiple spaces to single space
      .replace(/\n{3,}/g, '\n\n')     // Multiple newlines to double newline
      .replace(/\t+/g, ' ')           // Tabs to spaces
      .trim();
  }

  /**
   * Extract key information from text
   */
  extractKeyInfo(text) {
    const info = {
      sentences: [],
      keywords: [],
      entities: []
    };

    // Extract sentences
    info.sentences = text.match(/[^.!?]+[.!?]+/g) || [];

    // Extract potential keywords (capitalized words)
    const words = text.split(/\s+/);
    info.keywords = words.filter(word => 
      word.length > 3 && 
      word[0] === word[0].toUpperCase() &&
      word !== word.toLowerCase()
    );

    return info;
  }

  /**
   * Validate chunk quality
   */
  validateChunk(chunk) {
    if (!chunk || !chunk.content) {
      return { valid: false, reason: 'No content' };
    }

    if (chunk.content.length < this.minChunkSize) {
      return { valid: false, reason: 'Chunk too small' };
    }

    if (chunk.content.length > this.maxChunkSize) {
      return { valid: false, reason: 'Chunk too large' };
    }

    // Check for meaningful content (not just special characters)
    const meaningfulChars = chunk.content.replace(/[^a-zA-Z0-9가-힣]/g, '').length;
    if (meaningfulChars < chunk.content.length * 0.3) {
      return { valid: false, reason: 'Not enough meaningful content' };
    }

    return { valid: true };
  }

  /**
   * Enhance chunk with additional metadata
   */
  enhanceChunk(chunk) {
    const info = this.extractKeyInfo(chunk.content);
    
    return {
      ...chunk,
      metadata: {
        ...chunk.metadata,
        sentenceCount: info.sentences.length,
        keywordCount: info.keywords.length,
        contentHash: this.generateHash(chunk.content)
      }
    };
  }

  /**
   * Generate simple hash for content
   */
  generateHash(content) {
    let hash = 0;
    for (let i = 0; i < content.length; i++) {
      const char = content.charCodeAt(i);
      hash = ((hash << 5) - hash) + char;
      hash = hash & hash; // Convert to 32bit integer
    }
    return hash.toString(16);
  }

  /**
   * Process and validate chunks
   */
  processChunks(chunks) {
    const validChunks = [];
    
    for (const chunk of chunks) {
      const validation = this.validateChunk(chunk);
      
      if (validation.valid) {
        const enhanced = this.enhanceChunk(chunk);
        validChunks.push(enhanced);
      } else {
        logger.warn(`Invalid chunk skipped`, { 
          chunkId: chunk.id, 
          reason: validation.reason 
        });
      }
    }

    logger.info(`Processed ${chunks.length} chunks, ${validChunks.length} valid`);
    return validChunks;
  }

  /**
   * Merge small chunks
   */
  mergeSmallChunks(chunks) {
    const merged = [];
    let currentMerged = null;

    for (const chunk of chunks) {
      if (chunk.content.length < this.minChunkSize) {
        if (currentMerged) {
          currentMerged.content += '\n\n' + chunk.content;
          currentMerged.metadata.mergedCount = (currentMerged.metadata.mergedCount || 1) + 1;
        } else {
          currentMerged = { ...chunk };
          currentMerged.metadata.mergedCount = 1;
        }
      } else {
        if (currentMerged) {
          merged.push(currentMerged);
          currentMerged = null;
        }
        merged.push(chunk);
      }
    }

    if (currentMerged) {
      merged.push(currentMerged);
    }

    return merged;
  }
}

module.exports = TextProcessor;
