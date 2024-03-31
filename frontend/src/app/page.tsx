"use client";
import { Input } from "@/components/ui/input";
import { Button } from "@/components/ui/button";
import { AvatarImage, AvatarFallback, Avatar } from "@/components/ui/avatar";
import React, { useState } from "react";
import axios from "axios";
import ReactMarkdown from "react-markdown";

interface Message {
    prompt: string;
    response: string;
}

export default function Home() {
    // State
    const [repo_path, set_repo_path] = useState("");
    const [curr_repo_path, set_curr_repo_path] = useState("");
    const [prompt, set_prompt] = useState("");
    const [answer, set_answer] = useState("");
    const [submitted_prompt, set_submitted_prompt] = useState(
        "How can I help you today?"
    );
    const [loading, set_loading] = useState(false);

    // Index Repo Request
    const index_repo = async () => {
        try {
            set_loading(true);
            const response = await axios.post(
                "http://127.0.0.1:8000/api/index-repo",
                { repo_path }
            );
            set_curr_repo_path(repo_path);
            set_loading(false);
            alert(response.data.message);
        } catch (error) {
            alert("Error indexing repo.");
        }
    };

    // Query LLM Request
    const query_llm = async () => {
        try {
            set_answer(""); // Clearing answer
            const response = await fetch("http://127.0.0.1:8000/api/chat", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify({
                    repo_path: curr_repo_path,
                    prompt,
                    messages: [],
                }),
            });
            set_prompt(""); // Clearing prompt
            set_submitted_prompt(prompt); // Setting submitted prompt

            if (!response.ok) {
                throw new Error(`HTTP error: ${response.status}`);
            }

            const reader = response.body.getReader();
            const text_decoder = new TextDecoder("utf-8");
            while (true) {
                const { done, value } = await reader.read();
                if (done) break;
                set_answer((answer) => answer + text_decoder.decode(value)); // Update the answer state
            }
        } catch (error) {
            alert("Error querying LLM.");
            console.error(error);
        }
    };

    return (
        <div className="min-h-screen bg-gray-100 p-8">
            <div className="max-w-4xl mx-auto">
                <div className="text-4xl font-semibold text-gray-900 mb-8">
                    Welcome to Doc Oc.
                </div>
                <div className="mb-6">
                    <div className="text-lg font-semibold text-gray-900 mb-2">
                        About:
                    </div>
                    <p className="text-gray-900">
                        Doc Oc is a codebase exploration tool that uses AI to
                        help you understand code better. It can answer questions
                        about code, provide code snippets, and even generate
                        documentation.
                    </p>
                </div>
                <div className="mb-6">
                    <div className="text-lg font-semibold text-gray-900 mb-2">
                        Instructions:
                    </div>
                    <ul className="list-disc pl-6">
                        <li>Step 1: Enter the owner and repo name below.</li>
                        <li>
                            Step 2: Wait for Doc Oc to finish exploring the code
                            base.
                        </li>
                        <li>Step 3: Now you're all set! Ask a question.</li>
                    </ul>
                </div>
                <div className="mb-6 flex w-full items-center space-x-4">
                    <Input
                        className="flex-1"
                        placeholder="owner/repo"
                        value={repo_path}
                        onChange={(e) => set_repo_path(e.target.value)}
                    />
                    <Button onClick={index_repo}>
                        {loading ? "Loading..." : "Index Repo"}
                    </Button>
                </div>

                <div className="rounded-lg bg-white p-6 shadow">
                    <div className="flex items-center space-x-2">
                        <Avatar>
                            <AvatarImage alt="Doc Oc" src="/doc-oc-logo.png" />
                            <AvatarFallback>DO</AvatarFallback>
                        </Avatar>
                        <div>
                            <div className="text-sm font-semibold text-gray-900">
                                {submitted_prompt}
                            </div>
                        </div>
                    </div>
                    <div className="mt-4 mb-6 border-l-4 border-cyan-300 pl-4 text-sm text-gray-900">
                        <ReactMarkdown children={answer} />
                    </div>
                    <div className="mt-6">
                        <Input
                            className="w-full"
                            placeholder="Enter a prompt here"
                            value={prompt}
                            onChange={(e) => set_prompt(e.target.value)}
                        />
                    </div>
                    <Button className="mt-4" onClick={query_llm}>
                        Submit
                    </Button>
                </div>
            </div>
        </div>
    );
}
