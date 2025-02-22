import { NextResponse } from 'next/server';
import { spawn } from 'child_process';

export async function POST(request: Request) {
  const { user_prompt, project_summary } = await request.json();

  return new Promise((resolve, reject) => {
    // Debug: Log the arguments you’re passing
    console.log('Spawning python with args:', user_prompt, project_summary);

    const pythonProcess = spawn('python', [
      '/Users/aarjavjain/Desktop/Dev/aienginehackathon/agility/epic_generation.py',
      user_prompt,
      project_summary
    ]);

    let stdoutData = '';
    let stderrData = '';

    pythonProcess.stdout.on('data', (data) => {
      stdoutData += data.toString();
    });

    pythonProcess.stderr.on('data', (data) => {
      stderrData += data.toString();
    });

    pythonProcess.on('close', (code) => {
      console.log('Python process closed with code:', code);
      if (code !== 0) {
        // Debug: Log the error details
        console.error('Python stderr:', stderrData);
        return reject(
          NextResponse.json(
            { error: `Python script exited with code ${code}`, stderr: stderrData },
            { status: 500 }
          )
        );
      }

      // Debug: Log the raw output so you can see if there's formatting issues
      console.log('Python stdout data:', stdoutData);

      try {
        const result = JSON.parse(stdoutData);
        return resolve(NextResponse.json(result));
      } catch (err) {
        console.error('JSON parse error:', err);
        return reject(
          NextResponse.json(
            { error: 'Failed to parse JSON from Python', rawOutput: stdoutData },
            { status: 500 }
          )
        );
      }
    });
  });
}
