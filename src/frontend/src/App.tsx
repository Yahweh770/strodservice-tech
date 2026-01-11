import React from 'react';
import { BrowserRouter as Router, Routes, Route, Link } from 'react-router-dom';
import { AppBar, Toolbar, Typography, Drawer, List, ListItem, ListItemText, Box } from '@mui/material';
import './App.css';
import PtoPage from './pages/PtoPage';

function App() {
  const drawerWidth = 240;

  return (
    <Router>
      <Box sx={{ display: 'flex' }}>
        <AppBar position="fixed" sx={{ zIndex: (theme) => theme.zIndex.drawer + 1 }}>
          <Toolbar>
            <Typography variant="h6" noWrap component="div">
              Строд-Сервис Технолоджи
            </Typography>
          </Toolbar>
        </AppBar>

        <Drawer
          variant="permanent"
          sx={{
            width: drawerWidth,
            flexShrink: 0,
            [`& .MuiDrawer-paper`]: { width: drawerWidth, boxSizing: 'border-box' },
          }}
        >
          <Toolbar />
          <List>
            <ListItem button component={Link} to="/pto">
              <ListItemText primary="ПТО (Производство работ)" />
            </ListItem>
          </List>
        </Drawer>

        <Box component="main" sx={{ flexGrow: 1, p: 3 }}>
          <Toolbar />
          <Routes>
            <Route path="/" element={
              <Box sx={{ textAlign: 'center', mt: 5 }}>
                <Typography variant="h4" gutterBottom>
                  Добро пожаловать в Строд-Сервис Технолоджи
                </Typography>
                <Typography variant="h6">
                  Выберите раздел в меню слева для начала работы
                </Typography>
              </Box>
            } />
            <Route path="/pto" element={<PtoPage />} />
          </Routes>
        </Box>
      </Box>
    </Router>
  );
}

export default App;