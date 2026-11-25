import * as fs from 'node:fs';
import * as path from 'node:path';
import { fileURLToPath } from 'node:url';

// Resolve script directory robustly in Node 22 ESM
const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

function main() {
    const srcPath = path.join(__dirname, 'entry.png');
    const defaultOut = '/output/entry.png';
    const outDir = process.env.MAKEFUN_OUTPUT_DIR;
    
    let destPath = defaultOut;
    if (outDir) {
        destPath = path.join(outDir, 'entry.png');
    }

    // Ensure destination directory exists
    const destDir = path.dirname(destPath);
    fs.mkdirSync(destDir, { recursive: true });

    // Read source entry.png and write to destination
    const data = fs.readFileSync(srcPath);
    fs.writeFileSync(destPath, data);
    console.log(`Successfully copied entry.png from ${srcPath} to ${destPath}`);
}

main();
