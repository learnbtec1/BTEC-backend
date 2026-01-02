import 'dart:convert';
import 'package:http/http.dart' as http;
import '../constants/api_constants.dart';

class ApiClient {
  String? _authToken;
  
  void setAuthToken(String token) => _authToken = token;
  
  Map<String, String> _getHeaders() => {
    'Content-Type': 'application/json',
    if (_authToken != null) 'Authorization': 'Bearer $_authToken',
  };
  
  Future<dynamic> post(String endpoint, {Map<String, dynamic>? body}) async {
    final uri = Uri.parse('${ApiConstants.apiBase}$endpoint');
    final response = await http.post(uri, headers: _getHeaders(), 
      body: body != null ? jsonEncode(body) : null);
    
    if (response.statusCode >= 200 && response.statusCode < 300) {
      return response.body.isEmpty ? null : jsonDecode(response.body);
    }
    throw Exception('Error ${response.statusCode}: ${response.body}');
  }
  
  Future<dynamic> get(String endpoint) async {
    final uri = Uri.parse('${ApiConstants.apiBase}$endpoint');
    final response = await http.get(uri, headers: _getHeaders());
    
    if (response.statusCode == 200) {
      return jsonDecode(response.body);
    }
    throw Exception('Error ${response.statusCode}');
  }
}