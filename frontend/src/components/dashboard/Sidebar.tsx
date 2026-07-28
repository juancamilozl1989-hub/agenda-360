import {
  Box,
  List,
  ListItemButton,
  ListItemIcon,
  ListItemText,
  Typography,
} from "@mui/material";

import DashboardIcon from "@mui/icons-material/Dashboard";
import EventAvailableIcon from "@mui/icons-material/EventAvailable";
import GroupsIcon from "@mui/icons-material/Groups";
import ContentCutIcon from "@mui/icons-material/ContentCut";
import PersonIcon from "@mui/icons-material/Person";
import AssessmentIcon from "@mui/icons-material/Assessment";
import SettingsIcon from "@mui/icons-material/Settings";

const menuItems = [
  {
    text: "Dashboard",
    icon: <DashboardIcon />,
  },
  {
    text: "Agenda",
    icon: <EventAvailableIcon />,
  },
  {
    text: "Clientes",
    icon: <GroupsIcon />,
  },
  {
    text: "Servicios",
    icon: <ContentCutIcon />,
  },
  {
    text: "Barberos",
    icon: <PersonIcon />,
  },
  {
    text: "Reportes",
    icon: <AssessmentIcon />,
  },
  {
    text: "Configuración",
    icon: <SettingsIcon />,
  },
];

export default function Sidebar() {
  return (
    <Box
      sx={{
        width: 260,
        height: "100vh",
        bgcolor: "#181818",
        color: "#FFF",
        display: "flex",
        flexDirection: "column",
        borderRight: "1px solid rgba(255,255,255,.08)",
      }}
    >
      {/* Logo */}

      <Box
        sx={{
          p: 4,
          borderBottom: "1px solid rgba(255,255,255,.08)",
        }}
      >
        <Typography
          variant="h5"
          fontWeight="bold"
          color="#D4AF37"
        >
          ✂ Agenda 360
        </Typography>

        <Typography
          variant="body2"
          color="#AAA"
        >
          Barber Management
        </Typography>
      </Box>

      {/* Menú */}

      <List sx={{ mt: 2 }}>

        {menuItems.map((item, index) => (

          <ListItemButton
            key={index}
            sx={{
              mx: 2,
              mb: 1,
              borderRadius: 3,

              "&:hover": {
                bgcolor: "rgba(212,175,55,.15)",
              },
            }}
          >
            <ListItemIcon
              sx={{
                color: "#D4AF37",
                minWidth: 40,
              }}
            >
              {item.icon}
            </ListItemIcon>

            <ListItemText
              primary={item.text}
            />

          </ListItemButton>

        ))}

      </List>

      {/* Usuario */}

      <Box
        sx={{
          mt: "auto",
          p: 3,
          borderTop: "1px solid rgba(255,255,255,.08)",
        }}
      >
        <Typography fontWeight="bold">
          Juan Camilo
        </Typography>

        <Typography
          variant="body2"
          color="#AAA"
        >
          Administrador
        </Typography>
      </Box>
    </Box>
  );
}