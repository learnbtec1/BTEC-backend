import { createBrowserRouter } from "react-router-dom";
import AppLayout from "@/layout/AppLayout";

// استيراد الصفحات
import Login from "@/pages"; // لأن index.tsx هو الصفحة الرئيسية داخل pages
import Dashboard from "@/pages/Dashboard";
import Upload from "@/pages/Upload";
import Results from "@/pages/Results";
import Students from "@/pages/Students";
import Assignments from "@/pages/Assignments";

export const router = createBrowserRouter([
  // صفحة تسجيل الدخول
  { path: "/login", element: <Login /> },

  // الصفحة الرئيسية (الداشبورد)
  {
    path: "/",
    element: (
      <AppLayout>
        <Dashboard />
      </AppLayout>
    ),
  },

  // صفحة الرفع
  {
    path: "/upload",
    element: (
      <AppLayout>
        <Upload />
      </AppLayout>
    ),
  },

  // صفحة النتائج
  {
    path: "/results",
    element: (
      <AppLayout>
        <Results />
      </AppLayout>
    ),
  },

  // صفحة الطلاب
  {
    path: "/students",
    element: (
      <AppLayout>
        <Students />
      </AppLayout>
    ),
  },

  // صفحة الواجبات
  {
    path: "/assignments",
    element: (
      <AppLayout>
        <Assignments />
      </AppLayout>
    ),
  },
]);