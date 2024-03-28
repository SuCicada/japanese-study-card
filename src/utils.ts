export async function importFile(path: RequestInfo | URL) {
    try {
        const response = await fetch(path);
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        const text = await response.text();
        console.log("importFile: ", path);
        return text;
    } catch (error) {
        console.error('Error fetching the file:', error);
    }
    return '';
}

export interface Card {
    Expression: string,
    Reading: string,
    Meaning: string,
    Notes?: string,
    Tags: string[]
}

export async function parseCards(file: RequestInfo | URL) {
    const text = await importFile(file);
    const lines = text.split('\n');
    const cards = lines.map(line => {
        const arr = line.split("　");
        const fileStr = file.toString()
        let baseName = fileStr.substring(fileStr.lastIndexOf('/') + 1);
        baseName = baseName.substring(0, baseName.lastIndexOf('.'));
        const tag = baseName.replace("　", "-").replace(" ", "-")
        const res: Card = {
            "Expression": arr[0],
            "Reading": arr[1],
            "Meaning": arr.length > 2 ? arr[2] : "",
            "Tags": [tag]
        }
        return res;
    });
    return cards;
}


export async function getAudio(str: string) {
    str = str.trim();
    if (str.length === 0) {
        // setOutput("");
        return;
    }

    try {
        const response = await fetch("http://asus.sucicada.me:41402/ttsapi/generate_audio", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({
                tts_engine: "gtts",
                text: str,
                language: "ja",
                speed: 1,
            }),
        });
        if (!response.ok) {
            throw new Error("Network response was not ok");
        }
        const data = await response.json();
        let sampling_rate = data["sampling_rate"];
        let audioBase64 = data["audio"];

        let audioLainBase64 = await getLainAudio(audioBase64)
        // let audioBase64 = audioBase64Str.split(',')[1]
        let arrayBuffer = Buffer.from(audioLainBase64, "base64");

        const blob = new Blob([arrayBuffer], {type: "audio/wav"});
        const audioUrl = URL.createObjectURL(blob);
        return audioUrl;
    } catch (error) {
        console.error(error);
    }
}

export async function getLainAudio(audio_base64: string) {
    const req_json = {
        "audio": audio_base64,
        "auto_predict_f0": true,
        "cluster_ratio": 0,
// # "tran":3
    }
    const url = 'http://asus.sucicada.me:17861/svcapi/audio_to_audio'

    try {
        const response = await fetch(url, {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify(req_json),
        });
        if (!response.ok) {
            throw new Error("Network response was not ok");
        }
        const data = await response.json();
        let sampling_rate = data["sampling_rate"];
        let audioBase64 = data["audio"];
        // let audioBase64 = audioBase64Str.split(',')[1]
        // let arrayBuffer = Buffer.from(audioBase64, "base64");
        // const blob = new Blob([arrayBuffer], {type: "audio/wav"});
        // const audioUrl = URL.createObjectURL(blob);
        // return audioUrl;
        return audioBase64;
    } catch (error) {
        console.error(error);
    }

}
