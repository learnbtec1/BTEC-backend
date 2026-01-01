import { Outlet } from 'react-router-dom'; // أو المكونات الخاصة بك

function App() {
  return (
    // هنا نضيف الكلاس الخاص بالخلفية المتحركة
    <div className="bg-future-dark min-h-screen text-foreground font-sans antialiased">
      {/* هنا محتوى تطبيقك */}
      <h1 className="text-3xl font-bold text-center pt-10 ai-core">BTEC NEXUS SYSTEM</h1>
      
      {/* مثال لبطاقة هولوغرافية */}
      <div className="p-10 flex justify-center">
        <div className="holo-card p-6 rounded-xl max-w-sm">
           <h2 className="text-xl text-cyan-400 mb-2">System Status</h2>
           <p className="text-gray-300">All systems operational. AI Core online.</p>
        </div>
      </div>

    </div>
  )
}

export default App