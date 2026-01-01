'use client'

import { ReactNode } from 'react'
import { ThemeProvider } from 'next-themes'

export function Providers({ children }: { children: ReactNode }) {
  return (
    <ThemeProvider attribute="class" defaultTheme="dark" enableSystem>
      {/* إذا كانت الملفات الأخرى جاهزة، يمكنك إضافتها هنا */}
      {children}
    </ThemeProvider>
  )
}