class ApiConstants {
  // Base URL configuration
  static const String baseUrl = String.fromEnvironment(
    'API_BASE_URL',
    defaultValue: 'http://localhost:8000',
  );
  
  static const String apiVersion = '/api/v1';
  static String get apiBase => '$baseUrl$apiVersion';
  
  // Endpoints
  static const String login = '/auth/login';
  static const String register = '/auth/register';
  static const String evaluateText = '/btec/evaluate-text';
  static const String evaluateAudio = '/btec/evaluate-audio';
  static const String getResults = '/btec/results';
  static const String uploadFile = '/btec/upload';
  
  // Timeouts
  static const Duration connectionTimeout = Duration(seconds: 30);
  static const Duration receiveTimeout = Duration(seconds: 30);
}
