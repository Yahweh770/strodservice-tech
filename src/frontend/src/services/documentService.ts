import axios from 'axios';

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000/api';

interface DocumentType {
  id: number;
  name: string;
  description?: string;
  created_at: string;
  updated_at?: string;
}

interface Document {
  id: number;
  doc_number: string;
  title: string;
  project_id: string;
  document_type_id: number;
  status: string;
  created_at: string;
  updated_at?: string;
  type?: DocumentType;
}

interface DocumentShipment {
  id: number;
  document_id: number;
  recipient: string;
  shipment_date: string;
  notes?: string;
  created_at: string;
}

interface DocumentReturn {
  id: number;
  document_id: number;
  return_date: string;
  condition: string;
  notes?: string;
  created_at: string;
}

interface DocumentDetailed extends Document {
  type: DocumentType;
  shipments: DocumentShipment[];
  returns: DocumentReturn[];
}

interface CreateDocumentRequest {
  doc_number: string;
  title: string;
  project_id: string;
  document_type_id: number;
}

interface CreateShipmentRequest {
  recipient: string;
  shipment_date: string;
  notes?: string;
}

interface CreateReturnRequest {
  return_date: string;
  condition: string;
  notes?: string;
}

class DocumentService {
  private api = axios.create({
    baseURL: API_BASE_URL,
    headers: {
      'Content-Type': 'application/json',
    },
  });

  // Get all documents
  async getAllDocuments() {
    try {
      const response = await this.api.get('/documents/');
      return response.data;
    } catch (error) {
      console.error('Error fetching documents:', error);
      throw error;
    }
  }

  // Get document by ID
  async getDocumentById(id: number) {
    try {
      const response = await this.api.get(`/documents/${id}`);
      return response.data as DocumentDetailed;
    } catch (error) {
      console.error(`Error fetching document ${id}:`, error);
      throw error;
    }
  }

  // Create a new document
  async createDocument(document: CreateDocumentRequest) {
    try {
      const response = await this.api.post('/documents/', document);
      return response.data as Document;
    } catch (error) {
      console.error('Error creating document:', error);
      throw error;
    }
  }

  // Update a document
  async updateDocument(id: number, document: Partial<CreateDocumentRequest>) {
    try {
      const response = await this.api.put(`/documents/${id}`, document);
      return response.data as Document;
    } catch (error) {
      console.error(`Error updating document ${id}:`, error);
      throw error;
    }
  }

  // Delete a document
  async deleteDocument(id: number) {
    try {
      const response = await this.api.delete(`/documents/${id}`);
      return response.data;
    } catch (error) {
      console.error(`Error deleting document ${id}:`, error);
      throw error;
    }
  }

  // Create a shipment for a document
  async createShipment(docId: number, shipment: CreateShipmentRequest) {
    try {
      const response = await this.api.post(
        `/documents/${docId}/shipments`,
        shipment
      );
      return response.data as DocumentShipment;
    } catch (error) {
      console.error('Error creating shipment:', error);
      throw error;
    }
  }

  // Create a return for a document
  async createReturn(docId: number, returnData: CreateReturnRequest) {
    try {
      const response = await this.api.post(
        `/documents/${docId}/returns`,
        returnData
      );
      return response.data as DocumentReturn;
    } catch (error) {
      console.error('Error creating return:', error);
      throw error;
    }
  }

  // Get shipments for a document
  async getDocumentShipments(docId: number) {
    try {
      const response = await this.api.get(`/documents/${docId}/shipments`);
      return response.data as DocumentShipment[];
    } catch (error) {
      console.error(`Error fetching shipments for document ${docId}:`, error);
      throw error;
    }
  }

  // Get returns for a document
  async getDocumentReturns(docId: number) {
    try {
      const response = await this.api.get(`/documents/${docId}/returns`);
      return response.data as DocumentReturn[];
    } catch (error) {
      console.error(`Error fetching returns for document ${docId}:`, error);
      throw error;
    }
  }

  // Search documents
  async searchDocuments(query: string, filters?: { project_id?: string; status?: string }) {
    try {
      const response = await this.api.post('/documents/search', {
        query_str: query,
        project_id: filters?.project_id,
        status: filters?.status
      });
      return response.data as Document[];
    } catch (error) {
      console.error('Error searching documents:', error);
      throw error;
    }
  }

  // Get all document types
  async getDocumentTypes() {
    try {
      const response = await this.api.get('/documents/types');
      return response.data as DocumentType[];
    } catch (error) {
      console.error('Error fetching document types:', error);
      throw error;
    }
  }

  // Create a new document type
  async createDocumentType(type: Omit<DocumentType, 'id' | 'created_at' | 'updated_at'>) {
    try {
      const response = await this.api.post('/documents/types', type);
      return response.data as DocumentType;
    } catch (error) {
      console.error('Error creating document type:', error);
      throw error;
    }
  }
}

export default new DocumentService();