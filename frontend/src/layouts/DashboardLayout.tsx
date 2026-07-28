import { Box } from "@mui/material";

import Sidebar from "../components/dashboard/Sidebar";
import Header from "../components/dashboard/Header";

interface Props {
  children: React.ReactNode;
}

export default function DashboardLayout({
  children,
}: Props) {
  return (
    <Box
      sx={{
        display: "flex",
        minHeight: "100vh",
        bgcolor: "#121212",
      }}
    >
      {/* Sidebar */}

      <Sidebar />

      {/* Contenido */}

      <Box
        sx={{
          flex: 1,
          display: "flex",
          flexDirection: "column",
        }}
      >
        <Header />

        <Box
          sx={{
            flex: 1,
            p: 4,
            overflow: "auto",
          }}
        >
          {children}
        </Box>
      </Box>
    </Box>
  );
}