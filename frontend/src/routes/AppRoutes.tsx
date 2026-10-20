import {
  BrowserRouter,
  Navigate,
  Route,
  Routes,
} from "react-router-dom";

import DashboardLayout from "../layouts/DashboardLayout";
import PrivateRoute from "./PrivateRoute";

import LoginPage from "../pages/Login/LoginPage";
import DashboardPage from "../pages/Dashboard/DashboardPage";
import AgendaPage from "../pages/Agenda/AgendaPage";

// Estas páginas las crearemos en el siguiente paso
import ClientesPage from "../pages/Clientes/ClientesPage.tsx";
import ServiciosPage from "../pages/Servicios/ServiciosPage.tsx";
import BarberosPage from "../pages/Barberos/BarberosPage.tsx";
import ReportesPage from "../pages/Reportes/ReportesPage.tsx";
import HorariosPage from "../pages/Horarios/HorariosPage.tsx";

export default function AppRoutes() {
  return (
    <BrowserRouter>
      <Routes>
        {/* Login (pública) */}
        <Route
          path="/"
          element={<LoginPage />}
        />

        {/* Dashboard */}
        <Route
          path="/dashboard"
          element={
            <PrivateRoute>
              <DashboardLayout>
                <DashboardPage />
              </DashboardLayout>
            </PrivateRoute>
          }
        />

        {/* Agenda */}
        <Route
          path="/agenda"
          element={
            <PrivateRoute>
              <DashboardLayout>
                <AgendaPage />
              </DashboardLayout>
            </PrivateRoute>
          }
        />

        {/* Clientes */}
        <Route
          path="/clientes"
          element={
            <PrivateRoute>
              <DashboardLayout>
                <ClientesPage />
              </DashboardLayout>
            </PrivateRoute>
          }
        />

        {/* Servicios */}
        <Route
          path="/servicios"
          element={
            <PrivateRoute>
              <DashboardLayout>
                <ServiciosPage />
              </DashboardLayout>
            </PrivateRoute>
          }
        />

        {/* Barberos */}
        <Route
          path="/barberos"
          element={
            <PrivateRoute>
              <DashboardLayout>
                <BarberosPage />
              </DashboardLayout>
            </PrivateRoute>
          }
        />

        {/* Horarios de atención */}
        <Route
          path="/horarios"
          element={
            <PrivateRoute>
              <DashboardLayout>
                <HorariosPage />
              </DashboardLayout>
            </PrivateRoute>
          }
        />

        {/* Reportes */}
        <Route
          path="/reportes"
          element={
            <PrivateRoute>
              <DashboardLayout>
                <ReportesPage />
              </DashboardLayout>
            </PrivateRoute>
          }
        />

        {/* Redirección */}
        <Route
          path="*"
          element={<Navigate to="/" replace />}
        />
      </Routes>
    </BrowserRouter>
  );
}