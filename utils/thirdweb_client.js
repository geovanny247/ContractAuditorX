// utils/thirdweb_client.js
import { createThirdwebClient } from "thirdweb";
import dotenv from "dotenv";
dotenv.config();

export const client = createThirdwebClient({
  clientId: "3c1baec646d89b0b284bbcb5a73e56b3",
  secretKey: process.env.THIRDWEB_SECRET_KEY
});
