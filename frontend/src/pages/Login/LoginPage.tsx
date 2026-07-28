import hero from "../../assets/hero.jpg";

import {
  Box,
  Button,
  Paper,
  Typography,
} from "@mui/material";

import EventAvailableIcon from "@mui/icons-material/EventAvailable";
import GroupsIcon from "@mui/icons-material/Groups";
import ContentCutIcon from "@mui/icons-material/ContentCut";
import PersonOutlineIcon from "@mui/icons-material/PersonOutline";
import LockOutlinedIcon from "@mui/icons-material/LockOutlined";

import CustomTextField from "../../components/forms/CustomTextField";

export default function LoginPage() {
  return (
    <Box
      sx={{
        minHeight: "100vh",
        display: "flex",
        backgroundColor: "#121212",
      }}
    >
      {/* ===========================
          Panel izquierdo
      =========================== */}

      <Box
        sx={{
          flex: 1,
          position: "relative",
          backgroundImage: `url(${hero})`,
          backgroundSize: "cover",
          backgroundPosition: "center",
          display: "flex",
          justifyContent: "center",
          alignItems: "center",
          overflow: "hidden",
        }}
      >
        {/* Fondo oscuro */}

        <Box
          sx={{
            position: "absolute",
            inset: 0,
            background:
              "linear-gradient(90deg, rgba(0,0,0,.55), rgba(0,0,0,.88))",
          }}
        />

        {/* Contenido */}

        <Box
          sx={{
            position: "relative",
            zIndex: 2,
            color: "#FFF",
            px: 8,
            maxWidth: 520,
          }}
        >
          <Typography
            sx={{
              color: "#D4AF37",
              fontSize: 18,
              letterSpacing: 4,
              fontWeight: 600,
              mb: 2,
            }}
          >
            BARBER MANAGEMENT
          </Typography>

          <Typography
            variant="h2"
            sx={{
              fontWeight: 700,
              lineHeight: 1.1,
              mb: 3,
            }}
          >
            Agenda 360
          </Typography>

          <Typography
            sx={{
              fontSize: 20,
              color: "#E0E0E0",
              mb: 6,
              lineHeight: 1.8,
            }}
          >
            Organiza tu barbería de forma sencilla, rápida y profesional.
          </Typography>

          {/* Beneficios */}

          <Box
            sx={{
              display: "flex",
              flexDirection: "column",
              gap: 3,
            }}
          >
            <Box
              sx={{
                display: "flex",
                alignItems: "center",
                gap: 2,
              }}
            >
              <EventAvailableIcon
                sx={{
                  color: "#D4AF37",
                  fontSize: 30,
                }}
              />

              <Typography fontSize={18}>
                Agenda inteligente de citas
              </Typography>
            </Box>

            <Box
              sx={{
                display: "flex",
                alignItems: "center",
                gap: 2,
              }}
            >
              <GroupsIcon
                sx={{
                  color: "#D4AF37",
                  fontSize: 30,
                }}
              />

              <Typography fontSize={18}>
                Gestión de clientes
              </Typography>
            </Box>

            <Box
              sx={{
                display: "flex",
                alignItems: "center",
                gap: 2,
              }}
            >
              <ContentCutIcon
                sx={{
                  color: "#D4AF37",
                  fontSize: 30,
                }}
              />

              <Typography fontSize={18}>
                Control de servicios y barberos
              </Typography>
            </Box>
          </Box>
        </Box>
      </Box>

      {/* ===========================
          Panel derecho
      =========================== */}

      <Box
        sx={{
          flex: 1,
          display: "flex",
          justifyContent: "center",
          alignItems: "center",
          backgroundColor: "#121212",
          p: 4,
        }}
      >
        <Paper
          elevation={0}
          sx={{
            width: 430,
            p: 5,
            borderRadius: 5,
            bgcolor: "#1E1E1E",
            border: "1px solid rgba(212,175,55,.25)",
            boxShadow: "0px 25px 60px rgba(0,0,0,.45)",
          }}
        >
          {/* Encabezado */}

          <Box
            sx={{
              display: "flex",
              flexDirection: "column",
              alignItems: "center",
              mb: 4,
            }}
          >
            <Box
              sx={{
                width: 75,
                height: 75,
                borderRadius: "50%",
                bgcolor: "#D4AF37",
                display: "flex",
                justifyContent: "center",
                alignItems: "center",
                mb: 3,
              }}
            >
              <ContentCutIcon
                sx={{
                  color: "#121212",
                  fontSize: 40,
                }}
              />
            </Box>

            <Typography
              variant="h4"
              sx={{
                fontWeight: "bold",
                color: "#FFF",
              }}
            >
              Bienvenido
            </Typography>

            <Typography
              sx={{
                color: "#BDBDBD",
                mt: 1,
              }}
            >
              Inicia sesión para acceder a Agenda 360
            </Typography>
          </Box>

          {/* Usuario */}

          <CustomTextField
            label="Usuario"
            margin="normal"
            icon={
              <PersonOutlineIcon
                sx={{
                  color: "#D4AF37",
                }}
              />
            }
          />

          {/* Contraseña */}

          <CustomTextField
            label="Contraseña"
            type="password"
            margin="normal"
            icon={
              <LockOutlinedIcon
                sx={{
                  color: "#D4AF37",
                }}
              />
            }
          />

          {/* Botón */}

          <Button
            fullWidth
            variant="contained"
            size="large"
            sx={{
              mt: 4,
              py: 1.6,
              fontWeight: "bold",
              fontSize: 16,
              bgcolor: "#D4AF37",
              color: "#121212",
              borderRadius: 3,
              transition: ".3s",

              "&:hover": {
                bgcolor: "#E5C04A",
                transform: "translateY(-2px)",
                boxShadow:
                  "0px 10px 25px rgba(212,175,55,.35)",
              },
            }}
          >
            Iniciar sesión
          </Button>
        </Paper>
      </Box>
    </Box>
  );
}