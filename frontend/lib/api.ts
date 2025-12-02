import axios from 'axios';

const API_BASE_URL = 'http://localhost:8000/api';

export const api = axios.create({
    baseURL: API_BASE_URL,
    headers: {
        'Content-Type': 'application/json',
    },
});

export interface InitResponse {
    status: string;
    name: string;
    path: string;
}

export interface StepResponse {
    status: string;
    output?: string;
    images?: any[];
    message?: string;
    image_path?: string;
    reference_prompt?: string;
}

export interface RegenerateReferenceResponse {
    status: string;
    image_path: string;
    updated_prompt: string;
}

export const initCharacter = async (name: string, description: string): Promise<InitResponse> => {
    const response = await api.post('/init', { name, description });
    return response.data;
};

export const generateStep = async (characterName: string, step: string, context: any): Promise<StepResponse> => {
    const response = await api.post('/generate', {
        character_name: characterName,
        step,
        context,
    });
    return response.data;
};

export const regenerateReference = async (
    characterName: string,
    currentPrompt: string,
    additionalInstruction: string
): Promise<RegenerateReferenceResponse> => {
    const response = await api.post('/regenerate-reference', {
        character_name: characterName,
        current_prompt: currentPrompt,
        additional_instruction: additionalInstruction,
    });
    return response.data;
};
