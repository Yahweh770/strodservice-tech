import React, { useState, useEffect } from 'react';
import {
  Box,
  Paper,
  Typography,
  TextField,
  Button,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  IconButton,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  Select,
  MenuItem,
  FormControl,
  InputLabel,
  Tabs,
  Tab,
  Alert,
  CircularProgress,
  Chip
} from '@mui/material';
import {
  Add as AddIcon,
  Edit as EditIcon,
  Delete as DeleteIcon,
  Send as SendIcon,
  Undo as UndoIcon,
  Close as CloseIcon
} from '@mui/icons-material';
import documentService from '../services/documentService';

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

const DocumentsPage: React.FC = () => {
  const [documents, setDocuments] = useState<Document[]>([]);
  const [documentTypes, setDocumentTypes] = useState<DocumentType[]>([]);
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);
  const [success, setSuccess] = useState<string | null>(null);
  const [activeTab, setActiveTab] = useState(0);
  
  // Form states
  const [showAddDialog, setShowAddDialog] = useState(false);
  const [showShipDialog, setShowShipDialog] = useState(false);
  const [showReturnDialog, setShowReturnDialog] = useState(false);
  
  // Document form fields
  const [docNumber, setDocNumber] = useState('');
  const [docTitle, setDocTitle] = useState('');
  const [projectId, setProjectId] = useState('');
  const [documentTypeId, setDocumentTypeId] = useState<number | null>(null);
  const [selectedDocumentId, setSelectedDocumentId] = useState<number | null>(null);
  
  // Shipment form fields
  const [recipient, setRecipient] = useState('');
  const [shipmentDate, setShipmentDate] = useState('');
  const [shipmentNotes, setShipmentNotes] = useState('');
  
  // Return form fields
  const [condition, setCondition] = useState('');
  const [returnNotes, setReturnNotes] = useState('');

  useEffect(() => {
    fetchAllData();
  }, []);

  const fetchAllData = async () => {
    try {
      setLoading(true);
      // Fetch both documents and document types
      const [docs, types] = await Promise.all([
        documentService.getAllDocuments(),
        documentService.getDocumentTypes()
      ]);
      
      setDocuments(docs);
      setDocumentTypes(types);
      setError(null);
    } catch (err) {
      setError('Ошибка при загрузке данных');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const handleAddDocument = async () => {
    if (!docNumber || !docTitle || !projectId || !documentTypeId) {
      setError('Все поля обязательны для заполнения');
      return;
    }

    try {
      const newDoc = await documentService.createDocument({
        doc_number: docNumber,
        title: docTitle,
        project_id: projectId,
        document_type_id: documentTypeId
      });
      
      setDocuments([...documents, newDoc]);
      setShowAddDialog(false);
      setSuccess('Документ успешно добавлен');
      resetForm();
    } catch (err) {
      setError('Ошибка при добавлении документа');
      console.error(err);
    }
  };

  const handleShipDocument = async () => {
    if (!selectedDocumentId || !recipient) {
      setError('Необходимо выбрать документ и указать получателя');
      return;
    }

    try {
      const shipment = await documentService.createShipment(selectedDocumentId, {
        recipient,
        shipment_date: shipmentDate || new Date().toISOString().split('T')[0],
        notes: shipmentNotes
      });
      
      // Update document status in local state
      setDocuments(documents.map(doc => 
        doc.id === selectedDocumentId ? { ...doc, status: 'shipped' } : doc
      ));
      
      setShowShipDialog(false);
      setSuccess('Документ успешно отправлен');
      resetShipmentForm();
    } catch (err) {
      setError('Ошибка при отправке документа');
      console.error(err);
    }
  };

  const handleReturnDocument = async () => {
    if (!selectedDocumentId || !condition) {
      setError('Необходимо выбрать документ и указать состояние');
      return;
    }

    try {
      const returnData = await documentService.createReturn(selectedDocumentId, {
        return_date: new Date().toISOString().split('T')[0],
        condition,
        notes: returnNotes
      });
      
      // Update document status in local state
      setDocuments(documents.map(doc => 
        doc.id === selectedDocumentId ? { ...doc, status: 'returned' } : doc
      ));
      
      setShowReturnDialog(false);
      setSuccess('Возврат документа успешно зафиксирован');
      resetReturnForm();
    } catch (err) {
      setError('Ошибка при возврате документа');
      console.error(err);
    }
  };

  const handleDeleteDocument = async (id: number) => {
    if (window.confirm('Вы уверены, что хотите удалить этот документ?')) {
      try {
        await documentService.deleteDocument(id);
        setDocuments(documents.filter(doc => doc.id !== id));
        setSuccess('Документ успешно удален');
      } catch (err) {
        setError('Ошибка при удалении документа');
        console.error(err);
      }
    }
  };

  const resetForm = () => {
    setDocNumber('');
    setDocTitle('');
    setProjectId('');
    setDocumentTypeId(null);
  };

  const resetShipmentForm = () => {
    setRecipient('');
    setShipmentDate('');
    setShipmentNotes('');
    setSelectedDocumentId(null);
  };

  const resetReturnForm = () => {
    setCondition('');
    setReturnNotes('');
    setSelectedDocumentId(null);
  };

  const handleTabChange = (event: React.SyntheticEvent, newValue: number) => {
    setActiveTab(newValue);
  };

  const getStatusColor = (status: string) => {
    switch (status.toLowerCase()) {
      case 'in_office':
        return '#4caf50'; // Green
      case 'shipped':
        return '#ff9800'; // Orange
      case 'returned':
        return '#2196f3'; // Blue
      default:
        return '#9e9e9e'; // Gray
    }
  };

  const getStatusLabel = (status: string) => {
    switch (status.toLowerCase()) {
      case 'in_office':
        return 'В офисе';
      case 'shipped':
        return 'Отправлен';
      case 'returned':
        return 'Возвращен';
      default:
        return status;
    }
  };

  if (loading) {
    return (
      <Box sx={{ display: 'flex', justifyContent: 'center', alignItems: 'center', height: '50vh' }}>
        <CircularProgress />
      </Box>
    );
  }

  return (
    <Box sx={{ flexGrow: 1, p: 3 }}>
      <Typography variant="h4" gutterBottom>
        Учет исполнительной документации
      </Typography>
      
      <Paper sx={{ p: 2, mb: 3 }}>
        <Tabs value={activeTab} onChange={handleTabChange}>
          <Tab label="Все документы" />
          <Tab label="Добавить документ" />
          <Tab label="Отправить документ" />
          <Tab label="Вернуть документ" />
        </Tabs>
      </Paper>

      {error && (
        <Alert severity="error" sx={{ mb: 2 }}>
          {error}
        </Alert>
      )}
      
      {success && (
        <Alert severity="success" sx={{ mb: 2 }} action={
          <IconButton
            aria-label="close"
            color="inherit"
            size="small"
            onClick={() => setSuccess(null)}
          >
            <CloseIcon fontSize="inherit" />
          </IconButton>
        }>
          {success}
        </Alert>
      )}

      {/* All Documents Tab */}
      {activeTab === 0 && (
        <Paper sx={{ p: 2 }}>
          <Typography variant="h6" gutterBottom>
            Список документов
          </Typography>
          
          <TableContainer>
            <Table>
              <TableHead>
                <TableRow>
                  <TableCell>ID</TableCell>
                  <TableCell>Номер</TableCell>
                  <TableCell>Наименование</TableCell>
                  <TableCell>Проект</TableCell>
                  <TableCell>Тип</TableCell>
                  <TableCell>Статус</TableCell>
                  <TableCell>Дата создания</TableCell>
                  <TableCell>Действия</TableCell>
                </TableRow>
              </TableHead>
              <TableBody>
                {documents.map((doc) => (
                  <TableRow key={doc.id}>
                    <TableCell>{doc.id}</TableCell>
                    <TableCell>{doc.doc_number}</TableCell>
                    <TableCell>{doc.title}</TableCell>
                    <TableCell>{doc.project_id}</TableCell>
                    <TableCell>{doc.type?.name || `ID: ${doc.document_type_id}`}</TableCell>
                    <TableCell>
                      <Chip 
                        label={getStatusLabel(doc.status)} 
                        sx={{ 
                          backgroundColor: getStatusColor(doc.status),
                          color: 'white',
                          fontWeight: 'bold'
                        }}
                      />
                    </TableCell>
                    <TableCell>{new Date(doc.created_at).toLocaleDateString()}</TableCell>
                    <TableCell>
                      <IconButton 
                        color="primary" 
                        onClick={() => {
                          setSelectedDocumentId(doc.id);
                          setShowShipDialog(true);
                        }}
                        disabled={doc.status !== 'in_office'}
                        title="Отправить документ"
                      >
                        <SendIcon />
                      </IconButton>
                      <IconButton 
                        color="secondary" 
                        onClick={() => {
                          setSelectedDocumentId(doc.id);
                          setShowReturnDialog(true);
                        }}
                        disabled={doc.status !== 'shipped'}
                        title="Вернуть документ"
                      >
                        <UndoIcon />
                      </IconButton>
                      <IconButton 
                        color="error" 
                        onClick={() => handleDeleteDocument(doc.id)}
                        title="Удалить документ"
                      >
                        <DeleteIcon />
                      </IconButton>
                    </TableCell>
                  </TableRow>
                ))}
              </TableBody>
            </Table>
          </TableContainer>
        </Paper>
      )}

      {/* Add Document Tab */}
      {activeTab === 1 && (
        <Paper sx={{ p: 2 }}>
          <Typography variant="h6" gutterBottom>
            Добавить новый документ
          </Typography>
          
          <Box sx={{ display: 'flex', flexDirection: 'column', gap: 2, maxWidth: 600 }}>
            <TextField
              label="Номер документа *"
              value={docNumber}
              onChange={(e) => setDocNumber(e.target.value)}
              required
            />
            <TextField
              label="Наименование документа *"
              value={docTitle}
              onChange={(e) => setDocTitle(e.target.value)}
              required
            />
            <TextField
              label="ID проекта *"
              value={projectId}
              onChange={(e) => setProjectId(e.target.value)}
              required
            />
            <FormControl fullWidth required>
              <InputLabel>Тип документа *</InputLabel>
              <Select
                value={documentTypeId || ''}
                onChange={(e) => setDocumentTypeId(Number(e.target.value))}
              >
                {documentTypes.map(type => (
                  <MenuItem key={type.id} value={type.id}>
                    {type.name}
                  </MenuItem>
                ))}
              </Select>
            </FormControl>
            
            <Button 
              variant="contained" 
              color="primary" 
              onClick={handleAddDocument}
              startIcon={<AddIcon />}
            >
              Добавить документ
            </Button>
          </Box>
        </Paper>
      )}

      {/* Ship Document Tab */}
      {activeTab === 2 && (
        <Paper sx={{ p: 2 }}>
          <Typography variant="h6" gutterBottom>
            Отправить документ
          </Typography>
          
          <Box sx={{ display: 'flex', flexDirection: 'column', gap: 2, maxWidth: 600 }}>
            <FormControl fullWidth required>
              <InputLabel>Документ</InputLabel>
              <Select
                value={selectedDocumentId || ''}
                onChange={(e) => setSelectedDocumentId(Number(e.target.value))}
              >
                {documents
                  .filter(doc => doc.status === 'in_office')
                  .map(doc => (
                    <MenuItem key={doc.id} value={doc.id}>
                      {doc.doc_number} - {doc.title} ({doc.project_id})
                    </MenuItem>
                  ))
                }
              </Select>
            </FormControl>
            
            <TextField
              label="Получатель *"
              value={recipient}
              onChange={(e) => setRecipient(e.target.value)}
              required
            />
            <TextField
              label="Дата отправки"
              type="date"
              value={shipmentDate || new Date().toISOString().split('T')[0]}
              onChange={(e) => setShipmentDate(e.target.value)}
              InputLabelProps={{
                shrink: true,
              }}
            />
            <TextField
              label="Примечания"
              multiline
              rows={3}
              value={shipmentNotes}
              onChange={(e) => setShipmentNotes(e.target.value)}
            />
            
            <Button 
              variant="contained" 
              color="primary" 
              onClick={handleShipDocument}
              startIcon={<SendIcon />}
              disabled={!selectedDocumentId || !recipient}
            >
              Отправить документ
            </Button>
          </Box>
        </Paper>
      )}

      {/* Return Document Tab */}
      {activeTab === 3 && (
        <Paper sx={{ p: 2 }}>
          <Typography variant="h6" gutterBottom>
            Вернуть документ
          </Typography>
          
          <Box sx={{ display: 'flex', flexDirection: 'column', gap: 2, maxWidth: 600 }}>
            <FormControl fullWidth required>
              <InputLabel>Документ</InputLabel>
              <Select
                value={selectedDocumentId || ''}
                onChange={(e) => setSelectedDocumentId(Number(e.target.value))}
              >
                {documents
                  .filter(doc => doc.status === 'shipped')
                  .map(doc => (
                    <MenuItem key={doc.id} value={doc.id}>
                      {doc.doc_number} - {doc.title} ({doc.project_id})
                    </MenuItem>
                  ))
                }
              </Select>
            </FormControl>
            
            <TextField
              label="Состояние документа *"
              value={condition}
              onChange={(e) => setCondition(e.target.value)}
              required
            />
            <TextField
              label="Примечания"
              multiline
              rows={3}
              value={returnNotes}
              onChange={(e) => setReturnNotes(e.target.value)}
            />
            
            <Button 
              variant="contained" 
              color="secondary" 
              onClick={handleReturnDocument}
              startIcon={<UndoIcon />}
              disabled={!selectedDocumentId || !condition}
            >
              Зафиксировать возврат
            </Button>
          </Box>
        </Paper>
      )}

      {/* Add Document Dialog */}
      <Dialog open={showAddDialog} onClose={() => setShowAddDialog(false)}>
        <DialogTitle>Добавить новый документ</DialogTitle>
        <DialogContent>
          <Box sx={{ display: 'flex', flexDirection: 'column', gap: 2, mt: 2 }}>
            <TextField
              label="Номер документа *"
              value={docNumber}
              onChange={(e) => setDocNumber(e.target.value)}
              required
              autoFocus
            />
            <TextField
              label="Наименование документа *"
              value={docTitle}
              onChange={(e) => setDocTitle(e.target.value)}
              required
            />
            <TextField
              label="ID проекта *"
              value={projectId}
              onChange={(e) => setProjectId(e.target.value)}
              required
            />
            <FormControl fullWidth required>
              <InputLabel>Тип документа *</InputLabel>
              <Select
                value={documentTypeId || ''}
                onChange={(e) => setDocumentTypeId(Number(e.target.value))}
              >
                {documentTypes.map(type => (
                  <MenuItem key={type.id} value={type.id}>
                    {type.name}
                  </MenuItem>
                ))}
              </Select>
            </FormControl>
          </Box>
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setShowAddDialog(false)}>Отмена</Button>
          <Button onClick={handleAddDocument} variant="contained">Добавить</Button>
        </DialogActions>
      </Dialog>

      {/* Ship Document Dialog */}
      <Dialog open={showShipDialog} onClose={() => setShowShipDialog(false)}>
        <DialogTitle>Отправить документ</DialogTitle>
        <DialogContent>
          <Box sx={{ display: 'flex', flexDirection: 'column', gap: 2, mt: 2 }}>
            <TextField
              label="Получатель *"
              value={recipient}
              onChange={(e) => setRecipient(e.target.value)}
              required
              autoFocus
            />
            <TextField
              label="Дата отправки"
              type="date"
              value={shipmentDate || new Date().toISOString().split('T')[0]}
              onChange={(e) => setShipmentDate(e.target.value)}
              InputLabelProps={{
                shrink: true,
              }}
            />
            <TextField
              label="Примечания"
              multiline
              rows={3}
              value={shipmentNotes}
              onChange={(e) => setShipmentNotes(e.target.value)}
            />
          </Box>
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setShowShipDialog(false)}>Отмена</Button>
          <Button 
            onClick={handleShipDocument} 
            variant="contained" 
            color="primary"
            disabled={!recipient}
          >
            Отправить
          </Button>
        </DialogActions>
      </Dialog>

      {/* Return Document Dialog */}
      <Dialog open={showReturnDialog} onClose={() => setShowReturnDialog(false)}>
        <DialogTitle>Вернуть документ</DialogTitle>
        <DialogContent>
          <Box sx={{ display: 'flex', flexDirection: 'column', gap: 2, mt: 2 }}>
            <TextField
              label="Состояние документа *"
              value={condition}
              onChange={(e) => setCondition(e.target.value)}
              required
              autoFocus
            />
            <TextField
              label="Примечания"
              multiline
              rows={3}
              value={returnNotes}
              onChange={(e) => setReturnNotes(e.target.value)}
            />
          </Box>
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setShowReturnDialog(false)}>Отмена</Button>
          <Button 
            onClick={handleReturnDocument} 
            variant="contained" 
            color="secondary"
            disabled={!condition}
          >
            Зафиксировать возврат
          </Button>
        </DialogActions>
      </Dialog>
    </Box>
  );
};

export default DocumentsPage;