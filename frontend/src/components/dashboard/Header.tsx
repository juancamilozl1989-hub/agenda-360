import {
  AppBar,
  Avatar,
  Badge,
  Box,
  IconButton,
  TextField,
  Toolbar,
  Typography,
  InputAdornment,
} from "@mui/material";

import SearchIcon from "@mui/icons-material/Search";
import NotificationsNoneIcon from "@mui/icons-material/NotificationsNone";

export default function Header() {
  return (
    <AppBar
      position="static"
      elevation={0}
      sx={{
        bgcolor: "#181818",
        borderBottom: "1px solid rgba(255,255,255,.08)",
      }}
    >
      <Toolbar
        sx={{
          display: "flex",
          justifyContent: "space-between",
          minHeight: "80px",
        }}
      >
        {/* Título */}
        <Box>
          <Typography
            variant="h5"
            fontWeight="bold"
          >
            Dashboard
          </Typography>

          <Typography
            variant="body2"
            color="gray"
          >
            Resumen general del negocio
          </Typography>
        </Box>

        {/* Acciones */}
        <Box
          sx={{
            display: "flex",
            alignItems: "center",
            gap: 3,
          }}
        >
          {/* Buscar */}
          <TextField
            placeholder="Buscar..."
            size="small"
            sx={{
              width: 260,

              "& .MuiOutlinedInput-root": {
                bgcolor: "#222",
                borderRadius: 3,

                "& fieldset": {
                  borderColor: "#333",
                },

                "&:hover fieldset": {
                  borderColor: "#D4AF37",
                },

                "&.Mui-focused fieldset": {
                  borderColor: "#D4AF37",
                },
              },
            }}
            slotProps={{
              input: {
                startAdornment: (
                  <InputAdornment position="start">
                    <SearchIcon sx={{ color: "#D4AF37" }} />
                  </InputAdornment>
                ),
              },
            }}
          />

          {/* Notificaciones */}
          <IconButton
            sx={{
              color: "#FFF",
            }}
          >
            <Badge
              badgeContent={3}
              color="error"
            >
              <NotificationsNoneIcon />
            </Badge>
          </IconButton>

          {/* Usuario */}
          <Box
            sx={{
              display: "flex",
              alignItems: "center",
              gap: 2,
            }}
          >
            <Avatar
              sx={{
                bgcolor: "#D4AF37",
                color: "#121212",
                fontWeight: "bold",
              }}
            >
              C
            </Avatar>

            <Box>
              <Typography
                fontWeight="bold"
              >
                Juan Camilo
              </Typography>

              <Typography
                variant="body2"
                color="gray"
              >
                Administrador
              </Typography>
            </Box>
          </Box>
        </Box>
      </Toolbar>
    </AppBar>
  );
}