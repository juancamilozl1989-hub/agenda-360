import { createTheme } from "@mui/material/styles";

const theme = createTheme({
  palette: {
    mode: "dark",

    primary: {
      main: "#C9A227", // Dorado
    },

    secondary: {
      main: "#1E1E1E", // Gris oscuro
    },

    background: {
      default: "#121212",
      paper: "#1E1E1E",
    },

    text: {
      primary: "#FFFFFF",
      secondary: "#BDBDBD",
    },
  },

  typography: {
    fontFamily: [
      "Poppins",
      "Roboto",
      "Arial",
      "sans-serif",
    ].join(","),
  },

  shape: {
    borderRadius: 12,
  },
});

export default theme;