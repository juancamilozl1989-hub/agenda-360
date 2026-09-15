import {
  createContext,
  useContext,
  useState,
  type ReactNode,
} from "react";

import { login as loginRequest } from "../api/authService";

interface AuthContextType {
  isAuthenticated: boolean;
  userEmail: string | null;
  login: (email: string, password: string) => Promise<void>;
  logout: () => void;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

interface Props {
  children: ReactNode;
}

export function AuthProvider({ children }: Props) {
  const [token, setToken] = useState<string | null>(
    localStorage.getItem("agenda360_token")
  );

  const [userEmail, setUserEmail] = useState<string | null>(
    localStorage.getItem("agenda360_user")
  );

  async function login(email: string, password: string) {
    const data = await loginRequest(email, password);

    localStorage.setItem("agenda360_token", data.access_token);
    localStorage.setItem("agenda360_user", email);

    setToken(data.access_token);
    setUserEmail(email);
  }

  function logout() {
    localStorage.removeItem("agenda360_token");
    localStorage.removeItem("agenda360_user");

    setToken(null);
    setUserEmail(null);
  }

  return (
    <AuthContext.Provider
      value={{
        isAuthenticated: Boolean(token),
        userEmail,
        login,
        logout,
      }}
    >
      {children}
    </AuthContext.Provider>
  );
}

export function useAuth() {
  const context = useContext(AuthContext);

  if (!context) {
    throw new Error("useAuth debe usarse dentro de un AuthProvider");
  }

  return context;
}
