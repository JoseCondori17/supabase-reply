'use client'
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { files } from "@/constants/data";
import Editor from '@monaco-editor/react';

export function MonacoEditor() {
  return (
    <>
      <Tabs defaultValue="account" className="w-full">
        <TabsList>
          {files.map((file) => (
            <TabsTrigger value={file.name}>{file.name}</TabsTrigger>
          ))}
        </TabsList>
        <TabsContent value="file1">
          gola
        </TabsContent>
      </Tabs>
      <Editor
        height='100%'
        defaultLanguage='pgsql'
        defaultValue="-- write your script"
      />
    </>
  );
}