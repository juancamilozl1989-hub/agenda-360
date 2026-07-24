import {
  Box,
  Button,
  Container,
  Typography,
} from "@mui/material";

function App() {
  return (
    <Box
      sx={{
        minHeight: "100vh",
        bgcolor: "#121212",
        color: "#fff",
        display: "flex",
        alignItems: "center",
      }}
    >
      <Container maxWidth="md">

        <Typography
          variant="h2"
          sx={{
              fontWeight: "bold",
              color: "#C9A227",
          }}
>
          Agenda 360
        </Typography>

        <Typography
          variant="h5"
          sx={{
            mt: 2,
            mb: 4,
            color: "#d5d5d5",
          }}
        >
          Sistema inteligente para la gestión de citas y
          automatización de procesos mediante WhatsApp.
        </Typography>

        <Button
          variant="contained"
          sx={{
            bgcolor: "#C9A227",
            color: "#000",
            px: 5,
            py: 1.5,
            fontWeight: "bold",

            "&:hover": {
              bgcolor: "#b8901e",
            },
          }}
        >
          Iniciar sesión
        </Button>

      </Container>
    </Box>
  );
}

export default App;