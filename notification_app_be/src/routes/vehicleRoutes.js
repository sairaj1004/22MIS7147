const express = require("express");

const router = express.Router();

const {
    fetchVehicles,
    fetchDepots
} = require("../services/apiService");

const Log = require("../utils/logger");

router.get("/vehicles", async (req, res) => {

    try {

        await Log(
            "backend",
            "info",
            "route",
            "Fetching vehicles data"
        );

        const data = await fetchVehicles();

        res.status(200).json(data);

    } catch (error) {

        await Log(
            "backend",
            "error",
            "route",
            "Error while fetching vehicles"
        );

        res.status(500).json({
            message: error.message
        });
    }
});

router.get("/depots", async (req, res) => {

    try {

        await Log(
            "backend",
            "info",
            "route",
            "Fetching depots data"
        );

        const data = await fetchDepots();

        res.status(200).json(data);

    } catch (error) {

        await Log(
            "backend",
            "error",
            "route",
            "Error while fetching depots"
        );

        res.status(500).json({
            message: error.message
        });
    }
});

module.exports = router;