"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";
import { motion } from "framer-motion";
import { ArrowRight, Sparkles } from "lucide-react";
import { initCharacter } from "@/lib/api";

export default function Home() {
  const router = useRouter();
  const [name, setName] = useState("");
  const [desc, setDesc] = useState("");
  const [loading, setLoading] = useState(false);

  const handleStart = async () => {
    if (!name || !desc) return;
    setLoading(true);
    try {
      await initCharacter(name, desc);
      // Store initial data in localStorage to pass to wizard
      localStorage.setItem("char_name", name);
      localStorage.setItem("char_desc", desc);
      router.push("/create");
    } catch (error) {
      console.error(error);
      alert("Failed to initialize character. Is the backend running?");
    } finally {
      setLoading(false);
    }
  };

  return (
    <main className="flex min-h-screen flex-col items-center justify-center p-24 bg-black text-white selection:bg-purple-500 selection:text-white">
      <div className="z-10 max-w-5xl w-full items-center justify-between font-mono text-sm lg:flex">
        <p className="fixed left-0 top-0 flex w-full justify-center border-b border-gray-800 bg-black/50 pb-6 pt-8 backdrop-blur-2xl lg:static lg:w-auto lg:rounded-xl lg:border lg:bg-gray-900/50 lg:p-4">
          Gemini Ecosystem &nbsp;
          <code className="font-mono font-bold">Character Generator</code>
        </p>
      </div>

      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.8 }}
        className="relative flex place-items-center flex-col gap-8 mt-20"
      >
        <div className="text-center">
          <h1 className="text-6xl font-bold bg-clip-text text-transparent bg-gradient-to-r from-blue-400 via-purple-500 to-pink-500 pb-2">
            Create Life with AI
          </h1>
          <p className="mt-4 text-gray-400 text-xl max-w-2xl mx-auto">
            Powered by Google Gemini 3.0 Pro, Imagen 3, and Veo.
            Design deep, consistent characters with a single prompt.
          </p>
        </div>

        <div className="w-full max-w-md space-y-4 bg-gray-900/50 p-8 rounded-2xl border border-gray-800 backdrop-blur-sm">
          <div>
            <label className="block text-sm font-medium text-gray-400 mb-1">Character Name</label>
            <input
              type="text"
              value={name}
              onChange={(e) => setName(e.target.value)}
              className="w-full bg-gray-950 border border-gray-800 rounded-lg px-4 py-3 text-white focus:ring-2 focus:ring-purple-500 focus:border-transparent outline-none transition-all"
              placeholder="e.g. Nova"
            />
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-400 mb-1">Description</label>
            <textarea
              value={desc}
              onChange={(e) => setDesc(e.target.value)}
              className="w-full bg-gray-950 border border-gray-800 rounded-lg px-4 py-3 text-white focus:ring-2 focus:ring-purple-500 focus:border-transparent outline-none transition-all h-32 resize-none"
              placeholder="A cyberpunk hacker living in Neo-Seoul..."
            />
          </div>

          <button
            onClick={handleStart}
            disabled={loading || !name || !desc}
            className="w-full group relative flex items-center justify-center gap-2 bg-white text-black font-bold py-4 rounded-lg hover:bg-gray-200 transition-all disabled:opacity-50 disabled:cursor-not-allowed"
          >
            {loading ? (
              <span className="animate-pulse">Initializing...</span>
            ) : (
              <>
                Start Creation <ArrowRight className="w-4 h-4 group-hover:translate-x-1 transition-transform" />
              </>
            )}
          </button>
        </div>
      </motion.div>

      <div className="mb-32 grid text-center lg:max-w-5xl lg:w-full lg:mb-0 lg:grid-cols-3 lg:text-left mt-20 gap-4">
        {[
          { title: "Gemini 3.0 Pro", desc: "Advanced reasoning for deep character psychology and story arcs." },
          { title: "Imagen 3", desc: "Photorealistic image generation for consistent visual identity." },
          { title: "Veo Video", desc: "Bring your character to life with cinematic motion prompts." },
        ].map((item, i) => (
          <div key={i} className="group rounded-lg border border-transparent px-5 py-4 transition-colors hover:border-gray-700 hover:bg-gray-900/30">
            <h2 className={`mb-3 text-2xl font-semibold flex items-center gap-2`}>
              {item.title}
              <Sparkles className="w-4 h-4 text-purple-500" />
            </h2>
            <p className={`m-0 max-w-[30ch] text-sm opacity-50`}>
              {item.desc}
            </p>
          </div>
        ))}
      </div>
    </main>
  );
}
