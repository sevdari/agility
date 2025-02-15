"use client"

import { cn } from "@/lib/utils"
import { motion } from "framer-motion"
import type { ReactNode } from "react"

interface InitialViewProps {
  children: ReactNode
  className?: string
}

export function InitialView({ children, className }: InitialViewProps) {
  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      exit={{ opacity: 0, y: -20 }}
      className={cn("flex flex-col items-center justify-center flex-1", className)}
    >
      <h1 className="text-4xl font-bold mb-8">What are you developing?</h1>
      {children}
    </motion.div>
  )
}

