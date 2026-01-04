# Keitagorus Frontend Components

This directory contains React/TypeScript components for the Keitagorus AI learning assistant platform.

## Components

### ChatWidget

An interactive chat interface for communicating with the Keitagorus AI assistant.

**Features:**
- Real-time messaging with AI assistant
- Bilingual support (English/Arabic)
- Display of AI recommendations and suggested actions
- Typing indicators
- Message history
- Auto-scroll to latest message

**Usage:**

```tsx
import { ChatWidget } from '@/components/ChatWidget';

function MyPage() {
  const [authToken, setAuthToken] = useState<string>('');

  return (
    <ChatWidget
      apiBaseUrl="http://localhost:8000/api/v1"
      authToken={authToken}
      className="w-full"
    />
  );
}
```

**Props:**
- `apiBaseUrl` (optional): Backend API base URL (default: `http://localhost:8000/api/v1`)
- `authToken` (optional): JWT authentication token
- `className` (optional): Additional CSS classes

### FileUpload

A drag-and-drop file upload component with progress tracking.

**Features:**
- Drag and drop support
- File type validation
- File size validation
- Upload progress indicator
- Success/error status display
- File preview

**Usage:**

```tsx
import { FileUpload } from '@/components/FileUpload';

function MyPage() {
  const [authToken, setAuthToken] = useState<string>('');

  const handleUploadSuccess = (file: any) => {
    console.log('File uploaded:', file);
  };

  const handleUploadError = (error: string) => {
    console.error('Upload error:', error);
  };

  return (
    <FileUpload
      apiBaseUrl="http://localhost:8000/api/v1"
      authToken={authToken}
      maxSizeMB={10}
      allowedTypes={['image/*', 'application/pdf', '.docx']}
      onUploadSuccess={handleUploadSuccess}
      onUploadError={handleUploadError}
    />
  );
}
```

**Props:**
- `apiBaseUrl` (optional): Backend API base URL
- `authToken` (optional): JWT authentication token
- `maxSizeMB` (optional): Maximum file size in MB (default: 10)
- `allowedTypes` (optional): Array of allowed MIME types or extensions (default: `['*']`)
- `onUploadSuccess` (optional): Callback on successful upload
- `onUploadError` (optional): Callback on upload error
- `className` (optional): Additional CSS classes

## Dependencies

These components use the following libraries:
- React 18+
- TypeScript
- Tailwind CSS
- lucide-react (for icons)

Make sure these are installed in your project:

```bash
npm install lucide-react
```

## Integration with Backend

Both components are designed to work with the Keitagorus backend API endpoints:

### Authentication
First, get an auth token:

```typescript
const response = await fetch('http://localhost:8000/api/v1/login/access-token', {
  method: 'POST',
  headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
  body: new URLSearchParams({
    username: 'student1@example.com',
    password: 'student123',
  }),
});

const { access_token } = await response.json();
```

### Using with ChatWidget

The ChatWidget automatically sends requests to `/assistant/query` endpoint:

```typescript
POST /api/v1/assistant/query
Authorization: Bearer {token}
Content-Type: application/json

{
  "prompt": "Help me with my progress",
  "context": null
}
```

### Using with FileUpload

The FileUpload component sends multipart form data to `/files/upload`:

```typescript
POST /api/v1/files/upload
Authorization: Bearer {token}
Content-Type: multipart/form-data

file: [binary data]
```

## Styling

Both components use Tailwind CSS utility classes. Make sure Tailwind is configured in your project:

```bash
npm install -D tailwindcss postcss autoprefixer
npx tailwindcss init -p
```

Update your `tailwind.config.js`:

```javascript
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {},
  },
  plugins: [],
}
```

## Accessibility

Both components follow accessibility best practices:
- Keyboard navigation support
- ARIA labels where appropriate
- Focus management
- Screen reader friendly

## Future Enhancements

- [ ] WebSocket support for real-time streaming responses
- [ ] Voice input for ChatWidget
- [ ] Multiple file upload support
- [ ] File preview for common formats (PDF, images)
- [ ] Markdown rendering in chat messages
- [ ] Export chat history
- [ ] Multi-language UI translation

## License

See the main project LICENSE file.
