import 'dart:convert';
import 'dart:io';
import 'package:http/http.dart' as http;
import '../../../core/constants/api_constants.dart';
import '../models/assessment_model.dart';

class AssessmentService {
  String? _authToken;

  void setAuthToken(String token) {
    _authToken = token;
  }

  Map<String, String> _getHeaders() {
    return {
      'Content-Type': 'application/json',
      if (_authToken != null) 'Authorization': 'Bearer $_authToken',
    };
  }

  Future<AssessmentModel> evaluateText({
    required String studentAnswer,
    required String modelAnswer,
  }) async {
    final url = Uri.parse('${ApiConstants.apiBase}${ApiConstants.evaluateText}');
    
    final response = await http.post(
      url,
      headers: _getHeaders(),
      body: jsonEncode({
        'student_answer': studentAnswer,
        'model_answer': modelAnswer,
      }),
    ).timeout(ApiConstants.connectionTimeout);

    if (response.statusCode == 200 || response.statusCode == 201) {
      final data = jsonDecode(response.body);
      return AssessmentModel.fromJson(data);
    } else {
      throw Exception('فشل التقييم: ${response.body}');
    }
  }

  Future<String> evaluateAudio(File audioFile) async {
    final url = Uri.parse('${ApiConstants.apiBase}${ApiConstants.evaluateAudio}');
    
    final request = http.MultipartRequest('POST', url);
    if (_authToken != null) {
      request.headers['Authorization'] = 'Bearer $_authToken';
    }
    
    request.files.add(await http.MultipartFile.fromPath('file', audioFile.path));
    
    final streamedResponse = await request.send().timeout(ApiConstants.receiveTimeout);
    final response = await http.Response.fromStream(streamedResponse);

    if (response.statusCode == 200) {
      final data = jsonDecode(response.body);
      return data['transcription'] ?? data['text'] ?? '';
    } else {
      throw Exception('فشل تحليل الصوت: ${response.statusCode}');
    }
  }

  Future<List<AssessmentModel>> getResults() async {
    final url = Uri.parse('${ApiConstants.apiBase}${ApiConstants.getResults}');
    
    final response = await http.get(
      url,
      headers: _getHeaders(),
    ).timeout(ApiConstants.connectionTimeout);

    if (response.statusCode == 200) {
      final List<dynamic> data = jsonDecode(response.body);
      return data.map((json) => AssessmentModel.fromJson(json)).toList();
    } else {
      throw Exception('فشل جلب النتائج: ${response.statusCode}');
    }
  }
}
