import { Navigate } from "react-router-dom";
import type { ReactNode } from "react";

import { useAuth } from "../context/AuthContext";

interface Props {
  children: ReactNode;
}

// Envuelve cualquier página que requiera sesión iniciada.
// Si no hay token válido en el contexto, redirige al login.
export default function PrivateRoute({ children }: Props) {
  const { isAuthenticated } = useAuth();

  if (!isAuthenticated) {
    return <Navigate to="/" replace />;
  }

  return <>{children}</>;
}
