"use client";

import { useState, useEffect } from "react";
import { useRouter } from "next/navigation";
import { motion, AnimatePresence } from "framer-motion";
import ReactMarkdown from "react-markdown";
import {
    ArrowRight, ArrowLeft, Save, RefreshCw,
    User, BookOpen, Brain, Image as ImageIcon, Video, CheckCircle
} from "lucide-react";
import { generateStep, regenerateReference } from "@/lib/api";

const STEPS = [
    { id: "profile", name: "Character Design", icon: User },
    { id: "visual", name: "Visual Direction", icon: ImageIcon },
    { id: "story", name: "Story Foundation", icon: BookOpen },
    { id: "memories", name: "Memory Architect", icon: Brain },
    { id: "image_prompts", name: "Image Prompts", icon: ImageIcon },
    { id: "generate_reference", name: "Reference Image", icon: ImageIcon },
    { id: "generate_memories", name: "Memory Images", icon: ImageIcon },
    { id: "video_prompts", name: "Video Prompts", icon: Video },
    { id: "generate_videos", name: "Video Generation", icon: Video },
    { id: "review", name: "Final Review", icon: CheckCircle },
];

export default function CreatePage() {
    const router = useRouter();
    const [currentStepIdx, setCurrentStepIdx] = useState(0);
    const [loading, setLoading] = useState(false);
    const [charName, setCharName] = useState("");
    const [context, setContext] = useState<any>({});
    const [output, setOutput] = useState("");
    const [images, setImages] = useState<any[]>([]);
    const [referenceImage, setReferenceImage] = useState<string | null>(null);
    const [additionalInstruction, setAdditionalInstruction] = useState("");
    const [referencePrompt, setReferencePrompt] = useState("");

    useEffect(() => {
        const name = localStorage.getItem("char_name");
        const desc = localStorage.getItem("char_desc");
        if (!name || !desc) {
            router.push("/");
            return;
        }
        setCharName(name);
        setContext({ request: desc, char_name: name });

        // Auto-start first step
        handleGenerate("profile", { request: desc, char_name: name }, name);
    }, []);

    const handleGenerate = async (stepId: string, ctx: any, name: string) => {
        setLoading(true);
        try {
            const res = await generateStep(name, stepId, ctx);

            if (stepId === "generate_reference") {
                // Reference step: special handling
                if (res.image_path) {
                    setReferenceImage(res.image_path);
                    setReferencePrompt(res.reference_prompt || "");
                }
            } else if (res.output) {
                setOutput(res.output);
                setContext((prev: any) => ({ ...prev, [stepId]: res.output }));
            }

            if (res.images) {
                setImages(res.images);
            }
        } catch (error) {
            console.error(error);
            alert("Generation failed");
        } finally {
            setLoading(false);
        }
    };

    const handleRegenerateReference = async () => {
        if (!additionalInstruction.trim()) return;
        setLoading(true);
        try {
            const res = await regenerateReference(charName, referencePrompt, additionalInstruction);
            if (res.image_path) {
                setReferenceImage(res.image_path);
                setReferencePrompt(res.updated_prompt);
            }
            setAdditionalInstruction("");
        } catch (error) {
            console.error(error);
            alert("Regeneration failed");
        } finally {
            setLoading(false);
        }
    };

    const handleConfirmReference = async () => {
        setLoading(true);
        try {
            // Save confirmed prompt to context
            const updatedContext = {
                ...context,
                confirmed_reference_prompt: referencePrompt
            };
            setContext(updatedContext);

            // Move to next step (generate_memories)
            const nextIdx = currentStepIdx + 1;
            setCurrentStepIdx(nextIdx);

            // Generate memory images
            const res = await generateStep(charName, "generate_memories", updatedContext);
            if (res.images) {
                setImages(res.images);
            }
        } catch (error) {
            console.error(error);
            alert("Memory generation failed");
        } finally {
            setLoading(false);
        }
    };

    const handleNext = () => {
        const currentStep = STEPS[currentStepIdx];

        // generate_reference uses OK button, not Next
        if (currentStep.id === "generate_reference") {
            return;
        }

        // generate_memories shows images, skip auto-generate on next
        if (currentStep.id === "generate_memories") {
            if (currentStepIdx < STEPS.length - 1) {
                const nextIdx = currentStepIdx + 1;
                setCurrentStepIdx(nextIdx);
                const nextStep = STEPS[nextIdx];
                if (context[nextStep.id]) {
                    setOutput(context[nextStep.id]);
                } else {
                    setOutput("");
                    handleGenerate(nextStep.id, context, charName);
                }
            }
            return;
        }

        if (currentStepIdx < STEPS.length - 1) {
            const nextIdx = currentStepIdx + 1;
            setCurrentStepIdx(nextIdx);
            const nextStep = STEPS[nextIdx];

            // Clear output for next step unless already generated
            if (context[nextStep.id]) {
                setOutput(context[nextStep.id]);
            } else {
                setOutput("");
                handleGenerate(nextStep.id, context, charName);
            }
        } else {
            router.push("/gallery");
        }
    };

    const handlePrev = () => {
        if (currentStepIdx > 0) {
            const prevIdx = currentStepIdx - 1;
            setCurrentStepIdx(prevIdx);
            const prevStep = STEPS[prevIdx];
            setOutput(context[prevStep.id] || "");
        }
    };

    const currentStep = STEPS[currentStepIdx];

    return (
        <div className="min-h-screen bg-black text-white flex">
            {/* Sidebar */}
            <div className="w-64 border-r border-gray-800 p-6 hidden md:block">
                <h2 className="text-xl font-bold mb-8 text-purple-500">{charName}</h2>
                <div className="space-y-2">
                    {STEPS.map((step, idx) => {
                        const Icon = step.icon;
                        const isActive = idx === currentStepIdx;
                        const isCompleted = idx < currentStepIdx;
                        return (
                            <div
                                key={step.id}
                                className={`flex items-center gap-3 p-3 rounded-lg transition-colors ${isActive ? "bg-purple-900/30 text-purple-400" :
                                        isCompleted ? "text-green-400" : "text-gray-600"
                                    }`}
                            >
                                <Icon size={18} />
                                <span className="text-sm font-medium">{step.name}</span>
                                {isCompleted && <CheckCircle size={14} className="ml-auto" />}
                            </div>
                        );
                    })}
                </div>
            </div>

            {/* Main Content */}
            <div className="flex-1 flex flex-col h-screen overflow-hidden">
                <header className="border-b border-gray-800 p-6 flex justify-between items-center bg-black/50 backdrop-blur-md">
                    <h1 className="text-2xl font-bold flex items-center gap-3">
                        <currentStep.icon className="text-purple-500" />
                        {currentStep.name}
                    </h1>
                    <div className="flex gap-3">
                        <button
                            onClick={handlePrev}
                            disabled={currentStepIdx === 0 || loading}
                            className="px-4 py-2 rounded-lg border border-gray-700 hover:bg-gray-800 disabled:opacity-50"
                        >
                            <ArrowLeft size={20} />
                        </button>
                        <button
                            onClick={handleNext}
                            disabled={loading}
                            className="px-6 py-2 rounded-lg bg-white text-black font-bold hover:bg-gray-200 disabled:opacity-50 flex items-center gap-2"
                        >
                            {loading ? "Generating..." : "Next Step"}
                            {!loading && <ArrowRight size={20} />}
                        </button>
                    </div>
                </header>

                <main className="flex-1 overflow-auto p-8 relative">
                    {loading ? (
                        <div className="absolute inset-0 flex items-center justify-center bg-black/50 backdrop-blur-sm z-10">
                            <div className="flex flex-col items-center gap-4">
                                <div className="w-12 h-12 border-4 border-purple-500 border-t-transparent rounded-full animate-spin" />
                                <p className="text-purple-400 animate-pulse">Consulting Gemini 3.0...</p>
                            </div>
                        </div>
                    ) : null}

                    <AnimatePresence mode="wait">
                        <motion.div
                            key={currentStep.id}
                            initial={{ opacity: 0, x: 20 }}
                            animate={{ opacity: 1, x: 0 }}
                            exit={{ opacity: 0, x: -20 }}
                            className="max-w-4xl mx-auto"
                        >
                            {currentStep.id === "generate_reference" ? (
                                <div className="space-y-6">
                                    {/* Reference Image Display */}
                                    <div className="flex justify-center">
                                        {referenceImage ? (
                                            <div className="relative">
                                                <img
                                                    src={`http://localhost:8000${referenceImage}`}
                                                    alt="Reference"
                                                    className="max-w-md rounded-xl border border-gray-800"
                                                />
                                            </div>
                                        ) : (
                                            <div className="w-80 h-80 bg-gray-900 rounded-xl flex items-center justify-center border border-gray-800">
                                                <p className="text-gray-500">Generating reference...</p>
                                            </div>
                                        )}
                                    </div>

                                    {/* Modification Controls */}
                                    <div className="max-w-md mx-auto space-y-4">
                                        <textarea
                                            value={additionalInstruction}
                                            onChange={(e) => setAdditionalInstruction(e.target.value)}
                                            placeholder="수정 지시 입력 (예: 머리 더 짧게, 안경 없이, 더 밝은 표정...)"
                                            className="w-full p-3 bg-gray-900 border border-gray-700 rounded-lg text-white placeholder-gray-500 resize-none"
                                            rows={3}
                                        />
                                        <div className="flex gap-3">
                                            <button
                                                onClick={handleRegenerateReference}
                                                disabled={loading || !additionalInstruction.trim()}
                                                className="flex-1 px-4 py-3 bg-purple-600 hover:bg-purple-700 rounded-lg disabled:opacity-50 flex items-center justify-center gap-2 font-medium"
                                            >
                                                <RefreshCw size={16} />
                                                Regenerate
                                            </button>
                                            <button
                                                onClick={handleConfirmReference}
                                                disabled={loading || !referenceImage}
                                                className="flex-1 px-4 py-3 bg-green-600 hover:bg-green-700 rounded-lg disabled:opacity-50 flex items-center justify-center gap-2 font-medium"
                                            >
                                                <CheckCircle size={16} />
                                                OK, Generate Memories
                                            </button>
                                        </div>
                                    </div>

                                    {/* Current Prompt (collapsible) */}
                                    <details className="max-w-2xl mx-auto">
                                        <summary className="cursor-pointer text-gray-500 text-sm hover:text-gray-300">
                                            Current Prompt (click to view)
                                        </summary>
                                        <pre className="mt-2 p-4 bg-gray-900 rounded-lg text-xs overflow-auto text-gray-400 whitespace-pre-wrap">
                                            {referencePrompt}
                                        </pre>
                                    </details>
                                </div>
                            ) : currentStep.id === "generate_memories" ? (
                                <div className="grid grid-cols-2 md:grid-cols-3 gap-4">
                                    {images.map((img, i) => (
                                        <div key={i} className="aspect-square relative rounded-xl overflow-hidden border border-gray-800 group">
                                            {img.success ? (
                                                <img src={`http://localhost:8000${img.path}`} alt="Generated" className="w-full h-full object-cover" />
                                            ) : (
                                                <div className="w-full h-full flex items-center justify-center bg-gray-900 text-red-500">Failed</div>
                                            )}
                                            <div className="absolute bottom-0 left-0 right-0 bg-black/70 p-2 text-xs text-center opacity-0 group-hover:opacity-100 transition-opacity">
                                                Memory {img.id}
                                            </div>
                                        </div>
                                    ))}
                                </div>
                            ) : (
                                <div className="bg-gray-900/50 rounded-xl border border-gray-800 p-6">
                                    <div className="flex justify-between items-center mb-4">
                                        <span className="text-xs font-mono text-gray-500 uppercase">Output Preview</span>
                                        <button className="text-xs flex items-center gap-1 text-gray-400 hover:text-white">
                                            <Save size={14} /> Save Changes
                                        </button>
                                    </div>
                                    <textarea
                                        value={output}
                                        onChange={(e) => {
                                            setOutput(e.target.value);
                                            setContext((prev: any) => ({ ...prev, [currentStep.id]: e.target.value }));
                                        }}
                                        className="w-full h-[60vh] bg-transparent border-none outline-none font-mono text-sm resize-none"
                                    />
                                </div>
                            )}
                        </motion.div>
                    </AnimatePresence>
                </main>
            </div>
        </div>
    );
}
