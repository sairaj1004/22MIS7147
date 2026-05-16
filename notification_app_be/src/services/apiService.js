const axios = require("axios");
require("dotenv").config();

const token = process.env.ACCESS_TOKEN;

const headers = {
    Authorization: `Bearer ${token}`
};

const fetchVehicles = async () => {

    try {

        const response = await axios.get(
            "http://4.224.186.213/evaluation-service/vehicles",
            { headers }
        );

        return response.data;

    } catch (error) {

        console.log("FULL ERROR:");
        console.log(error.response?.data);
        console.log(error.response?.status);

        throw error;
    }
};

const fetchDepots = async () => {

    try {

        const response = await axios.get(
            "http://4.224.186.213/evaluation-service/depots",
            { headers }
        );

        return response.data;

    } catch (error) {

        console.log("FULL ERROR:");
        console.log(error.response?.data);
        console.log(error.response?.status);

        throw error;
    }
};

module.exports = {
    fetchVehicles,
    fetchDepots
};