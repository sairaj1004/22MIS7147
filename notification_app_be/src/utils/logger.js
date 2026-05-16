const axios = require("axios");
require("dotenv").config();

const token = process.env.ACCESS_TOKEN;

async function Log(stack, level, pkg, message) {

    try {

        const response = await axios.post(
            "http://4.224.186.213/evaluation-service/logs",
            {
                stack,
                level,
                package: pkg,
                message
            },
            {
                headers: {
                    Authorization: `Bearer ${token}`,
                    "Content-Type": "application/json"
                }
            }
        );

        console.log(response.data);

    } catch (error) {

        console.log(error.response?.data || error.message);

    }
}

module.exports = Log;