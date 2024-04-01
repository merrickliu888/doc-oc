import { AvatarImage, AvatarFallback, Avatar } from "@/components/ui/avatar";
import React from "react";
import ReactMarkdown from "react-markdown";

interface MyComponentProps {
    submitted_prompt: string;
    answer: string;
}

const MyComponent: React.FC<MyComponentProps> = ({
    submitted_prompt,
    answer,
}) => {
    return (
        <div className="rounded-lg bg-white p-6 shadow mb-6">
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
                <ReactMarkdown>{answer}</ReactMarkdown>
            </div>
        </div>
    );
};

export default MyComponent;
