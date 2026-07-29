import {
  Box,
  Button,
  Paper,
  Stack,
  Tab,
  Tabs,
  Typography,
} from "@mui/material";

import AddIcon from "@mui/icons-material/Add";

import TimeLine from "../../components/agenda/TimeLine";

export default function AgendaPage() {
  return (
    <Box>
      {/* Encabezado */}
      <Stack
        direction="row"
        justifyContent="space-between"
        alignItems="center"
        sx={{ mb: 4 }}
      >
        <Box>
          <Typography
            variant="h4"
            fontWeight="bold"
          >
            Agenda de Citas
          </Typography>

          <Typography color="text.secondary">
            Administra todas las citas de tu barbería.
          </Typography>
        </Box>

        <Button
          variant="contained"
          startIcon={<AddIcon />}
          sx={{
            bgcolor: "#D4AF37",
            color: "#121212",
            fontWeight: "bold",
            borderRadius: 3,
            px: 3,

            "&:hover": {
              bgcolor: "#E5C04A",
            },
          }}
        >
          Nueva cita
        </Button>
      </Stack>

      {/* Pestañas */}
      <Tabs
        value={0}
        sx={{
          mb: 3,

          "& .MuiTabs-indicator": {
            backgroundColor: "#D4AF37",
            height: 3,
            borderRadius: 2,
          },

          "& .MuiTab-root": {
            color: "#999",
            textTransform: "none",
            fontWeight: 600,
            fontSize: 15,
          },

          "& .Mui-selected": {
            color: "#D4AF37 !important",
          },
        }}
      >
        <Tab label="Hoy" />
        <Tab label="Semana" />
        <Tab label="Mes" />
      </Tabs>

      {/* Contenedor de la Agenda */}
      <Paper
        elevation={0}
        sx={{
          borderRadius: 4,
          bgcolor: "#1E1E1E",
          border: "1px solid rgba(255,255,255,.08)",
          p: 3,
        }}
      >
        <TimeLine />
      </Paper>
    </Box>
  );
}