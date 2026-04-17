/**
 * Vector Store
 * Manages storage and retrieval of document embeddings
 */

const logger = require('../utils/logger');
const fs = require('fs').promises;
const path = require('path');

class VectorStore {
  constructor(config) {
    this.config = config;
    this.storePath = path.join(config.vectorStorePath, 'vectors');
    this.indexPath = path.join(config.vectorStorePath, 'index.json');
    this.maxDocuments = config.maxDocuments || 1000;
    this.documents = [];
    this.index = {};
  }

  /**
   * Initialize vector store
   */
  async initialize() {
    try {
      await fs.mkdir(this.storePath, { recursive: true });
      await this.loadIndex();
      logger.info('Vector store initialized');
    } catch (error) {
      logger.error('Error initializing vector store', { error: error.message });
      throw error;
    }
  }

  /**
   * Store document chunks with embeddings
   */
  async store(chunks) {
    try {
      await this.initialize();

      const documentId = `doc-${Date.now()}-${Math.random().toString(36).substr(2, 9)}`;
      const docPath = path.join(this.storePath, `${documentId}.json`);

      const document = {
        id: documentId,
        chunks: chunks.map(chunk => ({
          id: chunk.id,
          content: chunk.content,
          embedding: chunk.embedding,
          metadata: chunk.metadata
        })),
        timestamp: new Date().toISOString(),
        chunkCount: chunks.length
      };

      // Save document to disk
      await fs.writeFile(docPath, JSON.stringify(document, null, 2));

      // Update index
      this.index[documentId] = {
        id: documentId,
        path: docPath,
        timestamp: document.timestamp,
        chunkCount: document.chunkCount,
        source: chunks[0]?.source
      };

      await this.saveIndex();

      logger.info(`Document stored successfully`, {
        documentId,
        chunkCount: chunks.length
      });

      return { id: documentId, chunkCount: chunks.length };
    } catch (error) {
      logger.error('Error storing document', { error: error.message });
      throw error;
    }
  }

  /**
   * Search for similar documents
   */
  async search(queryEmbedding, topK = 5, filter = {}) {
    try {
      await this.initialize();

      const results = [];
      const documentIds = Object.keys(this.index);

      for (const docId of documentIds) {
        const doc = await this.loadDocument(docId);
        
        if (!doc) continue;

        for (const chunk of doc.chunks) {
          // Apply filters
          if (filter.type && chunk.metadata.type !== filter.type) continue;
          if (filter.source && chunk.metadata.source !== filter.source) continue;

          // Calculate similarity
          const similarity = this.calculateCosineSimilarity(
            queryEmbedding,
            chunk.embedding
          );

          results.push({
            documentId: docId,
            chunkId: chunk.id,
            content: chunk.content,
            metadata: chunk.metadata,
            similarity
          });
        }
      }

      // Sort by similarity and return top K
      results.sort((a, b) => b.similarity - a.similarity);
      return results.slice(0, topK);
    } catch (error) {
      logger.error('Error searching vector store', { error: error.message });
      throw error;
    }
  }

  /**
   * Load document from disk
   */
  async loadDocument(documentId) {
    try {
      const docInfo = this.index[documentId];
      if (!docInfo) {
        logger.warn(`Document not found in index: ${documentId}`);
        return null;
      }

      const data = await fs.readFile(docInfo.path, 'utf8');
      return JSON.parse(data);
    } catch (error) {
      logger.error('Error loading document', { 
        documentId, 
        error: error.message 
      });
      return null;
    }
  }

  /**
   * Delete document from store
   */
  async deleteDocument(documentId) {
    try {
      const docInfo = this.index[documentId];
      if (!docInfo) {
        logger.warn(`Document not found: ${documentId}`);
        return false;
      }

      // Delete file
      await fs.unlink(docInfo.path);

      // Remove from index
      delete this.index[documentId];
      await this.saveIndex();

      logger.info(`Document deleted: ${documentId}`);
      return true;
    } catch (error) {
      logger.error('Error deleting document', { 
        documentId, 
        error: error.message 
      });
      throw error;
    }
  }

  /**
   * Save index to disk
   */
  async saveIndex() {
    try {
      await fs.writeFile(
        this.indexPath,
        JSON.stringify(this.index, null, 2),
        'utf8'
      );
    } catch (error) {
      logger.error('Error saving index', { error: error.message });
      throw error;
    }
  }

  /**
   * Load index from disk
   */
  async loadIndex() {
    try {
      const data = await fs.readFile(this.indexPath, 'utf8');
      this.index = JSON.parse(data);
      logger.info(`Loaded ${Object.keys(this.index).length} documents from index`);
    } catch (error) {
      // Index doesn't exist yet, create empty index
      this.index = {};
      await this.saveIndex();
    }
  }

  /**
   * Get store statistics
   */
  async getStats() {
    await this.initialize();

    const documentIds = Object.keys(this.index);
    let totalChunks = 0;

    for (const docId of documentIds) {
      totalChunks += this.index[docId].chunkCount;
    }

    return {
      totalDocuments: documentIds.length,
      totalChunks,
      maxDocuments: this.maxDocuments,
      availableSpace: this.maxDocuments - documentIds.length
    };
  }

  /**
   * Clear all documents from store
   */
  async clear() {
    try {
      const documentIds = Object.keys(this.index);

      for (const docId of documentIds) {
        await this.deleteDocument(docId);
      }

      logger.info('Vector store cleared');
    } catch (error) {
      logger.error('Error clearing vector store', { error: error.message });
      throw error;
    }
  }

  /**
   * Calculate cosine similarity
   */
  calculateCosineSimilarity(vec1, vec2) {
    if (vec1.length !== vec2.length) {
      throw new Error('Vector dimensions must match');
    }

    let dotProduct = 0;
    let magnitude1 = 0;
    let magnitude2 = 0;

    for (let i = 0; i < vec1.length; i++) {
      dotProduct += vec1[i] * vec2[i];
      magnitude1 += vec1[i] * vec1[i];
      magnitude2 += vec2[i] * vec2[i];
    }

    magnitude1 = Math.sqrt(magnitude1);
    magnitude2 = Math.sqrt(magnitude2);

    if (magnitude1 === 0 || magnitude2 === 0) {
      return 0;
    }

    return dotProduct / (magnitude1 * magnitude2);
  }

  /**
   * Export vector store data
   */
  async export(outputPath) {
    try {
      const stats = await this.getStats();
      const exportData = {
        stats,
        index: this.index,
        exportedAt: new Date().toISOString()
      };

      await fs.writeFile(outputPath, JSON.stringify(exportData, null, 2));
      logger.info(`Vector store exported to ${outputPath}`);
      return outputPath;
    } catch (error) {
      logger.error('Error exporting vector store', { error: error.message });
      throw error;
    }
  }
}

module.exports = VectorStore;
