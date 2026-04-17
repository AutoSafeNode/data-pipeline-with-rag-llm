/**
 * Embedding Generator
 * Generates embeddings for text chunks using various models
 */

const logger = require('../utils/logger');
const fs = require('fs').promises;
const path = require('path');

class EmbeddingGenerator {
  constructor(config) {
    this.config = config;
    this.embeddingModel = config.embeddingModel || 'text-embedding-004';
    this.cacheDir = path.join(config.vectorStorePath, 'cache');
  }

  /**
   * Generate embedding for a single text chunk
   */
  async generateEmbedding(text) {
    try {
      // For now, return a simple hash-based embedding
      // In production, this would call an actual embedding API
      const embedding = this.generateSimpleEmbedding(text);
      
      return embedding;
    } catch (error) {
      logger.error('Error generating embedding', { error: error.message });
      throw error;
    }
  }

  /**
   * Generate embeddings for multiple chunks
   */
  async generateEmbeddings(chunks) {
    try {
      logger.info(`Generating embeddings for ${chunks.length} chunks`);

      const chunksWithEmbeddings = [];

      for (const chunk of chunks) {
        const embedding = await this.generateEmbedding(chunk.content);
        
        chunksWithEmbeddings.push({
          ...chunk,
          embedding,
          metadata: {
            ...chunk.metadata,
            embeddingModel: this.embeddingModel,
            embeddingDimension: embedding.length
          }
        });
      }

      logger.info(`Generated embeddings for ${chunksWithEmbeddings.length} chunks`);
      return chunksWithEmbeddings;
    } catch (error) {
      logger.error('Error generating embeddings for chunks', { 
        error: error.message 
      });
      throw error;
    }
  }

  /**
   * Simple hash-based embedding (placeholder for production)
   * In production, use actual embedding models like:
   * - OpenAI embeddings
   * - Google Vertex AI embeddings
   * - HuggingFace transformers
   */
  generateSimpleEmbedding(text) {
    const dimension = 768; // Common embedding dimension
    const embedding = new Array(dimension);
    
    // Generate deterministic embedding based on text hash
    let hash = 0;
    for (let i = 0; i < text.length; i++) {
      const char = text.charCodeAt(i);
      hash = ((hash << 5) - hash) + char;
      hash = hash & hash;
    }
    
    // Use hash to seed a simple pseudo-random embedding
    for (let i = 0; i < dimension; i++) {
      const seed = hash + i * 31;
      embedding[i] = ((seed * seed * 1234567) % 1000000) / 1000000;
    }
    
    // Normalize embedding
    const magnitude = Math.sqrt(embedding.reduce((sum, val) => sum + val * val, 0));
    return embedding.map(val => val / magnitude);
  }

  /**
   * Calculate cosine similarity between two embeddings
   */
  calculateSimilarity(embedding1, embedding2) {
    if (embedding1.length !== embedding2.length) {
      throw new Error('Embedding dimensions must match');
    }

    let dotProduct = 0;
    let magnitude1 = 0;
    let magnitude2 = 0;

    for (let i = 0; i < embedding1.length; i++) {
      dotProduct += embedding1[i] * embedding2[i];
      magnitude1 += embedding1[i] * embedding1[i];
      magnitude2 += embedding2[i] * embedding2[i];
    }

    magnitude1 = Math.sqrt(magnitude1);
    magnitude2 = Math.sqrt(magnitude2);

    if (magnitude1 === 0 || magnitude2 === 0) {
      return 0;
    }

    return dotProduct / (magnitude1 * magnitude2);
  }

  /**
   * Find most similar chunks
   */
  async findSimilar(queryEmbedding, chunks, topK = 5) {
    const similarities = chunks.map(chunk => ({
      chunk,
      similarity: this.calculateSimilarity(queryEmbedding, chunk.embedding)
    }));

    similarities.sort((a, b) => b.similarity - a.similarity);

    return similarities.slice(0, topK);
  }

  /**
   * Cache embedding to disk
   */
  async cacheEmbedding(textHash, embedding) {
    try {
      await fs.mkdir(this.cacheDir, { recursive: true });
      const cachePath = path.join(this.cacheDir, `${textHash}.json`);
      await fs.writeFile(cachePath, JSON.stringify(embedding));
    } catch (error) {
      logger.warn('Failed to cache embedding', { error: error.message });
    }
  }

  /**
   * Load cached embedding
   */
  async loadCachedEmbedding(textHash) {
    try {
      const cachePath = path.join(this.cacheDir, `${textHash}.json`);
      const data = await fs.readFile(cachePath, 'utf8');
      return JSON.parse(data);
    } catch (error) {
      return null;
    }
  }

  /**
   * Batch generate embeddings with caching
   */
  async batchGenerateWithCache(chunks) {
    const results = [];
    const cacheHits = [];
    const cacheMisses = [];

    for (const chunk of chunks) {
      const textHash = chunk.metadata.contentHash;
      const cached = await this.loadCachedEmbedding(textHash);

      if (cached) {
        results.push({
          ...chunk,
          embedding: cached,
          metadata: {
            ...chunk.metadata,
            embeddingModel: this.embeddingModel,
            embeddingDimension: cached.length,
            cached: true
          }
        });
        cacheHits.push(chunk.id);
      } else {
        const embedding = await this.generateEmbedding(chunk.content);
        await this.cacheEmbedding(textHash, embedding);
        
        results.push({
          ...chunk,
          embedding,
          metadata: {
            ...chunk.metadata,
            embeddingModel: this.embeddingModel,
            embeddingDimension: embedding.length,
            cached: false
          }
        });
        cacheMisses.push(chunk.id);
      }
    }

    logger.info(`Batch embedding generation complete`, {
      total: chunks.length,
      cacheHits: cacheHits.length,
      cacheMisses: cacheMisses.length
    });

    return results;
  }
}

module.exports = EmbeddingGenerator;
