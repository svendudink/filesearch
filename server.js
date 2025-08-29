import path from "path";
import { fileURLToPath } from "url";
import fs from "fs/promises";

import express from "express";
import dotenv from "dotenv";
import OpenAI from "openai";

dotenv.config();

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

const app = express();
app.use(express.urlencoded({ extended: true }));
app.use("/images", express.static(path.join(__dirname, "images")));
app.set("view engine", "ejs");
app.set("views", path.join(__dirname, "templates"));

const client = new OpenAI({ apiKey: process.env.OPENAI_API_KEY });
const IMAGE_FOLDER = path.join(__dirname, "images");

async function imageContainsQuery(imagePath, query) {
  const buffer = await fs.readFile(imagePath);
  const imgB64 = buffer.toString("base64");

  const response = await client.responses.create({
    model: "gpt-4o-mini",
    input: [
      {
        role: "user",
        content: [
          { type: "input_text", text: `Does this image contain ${query}? Answer yes or no.` },
          { type: "input_image", image: imgB64 }
        ]
      }
    ]
  });
  const result = response.output_text.trim().toLowerCase();
  return result.includes("yes");
}

app.get("/", (req, res) => {
  res.render("index", { matches: [], query: "" });
});

app.post("/", async (req, res) => {
  const query = req.body.query || "";
  const files = await fs.readdir(IMAGE_FOLDER);
  const matches = [];
  for (const file of files) {
    const fullPath = path.join(IMAGE_FOLDER, file);
    const stat = await fs.stat(fullPath);
    if (stat.isFile()) {
      try {
        if (await imageContainsQuery(fullPath, query)) {
          matches.push(file);
        }
      } catch (err) {
        console.error(`Error processing ${file}: ${err.message}`);
      }
    }
  }
  res.render("index", { matches, query });
});

const port = process.env.PORT || 3000;
app.listen(port, () => {
  console.log(`Server running on http://localhost:${port}`);
});

