const express = require("express");

const vehicleRoutes = require("./routes/vehicleRoutes");

const app = express();

app.use(express.json());

app.get("/", (req, res) => {
    res.send("Backend server is running");
});

app.use("/api", vehicleRoutes);

module.exports = app;