import 'dart:convert';
import 'package:http/http.dart' as http;
import '../../../core/constants/api_constants.dart';
import '../models/user_model.dart';

class AuthService {
  Future<UserModel> login(String email, String password) async {
    final url = Uri.parse('${ApiConstants.apiBase}${ApiConstants.login}');
    
    final response = await http.post(
      url,
      headers: {'Content-Type': 'application/json'},
      body: jsonEncode({'email': email, 'password': password}),
    ).timeout(ApiConstants.connectionTimeout);

    if (response.statusCode == 200) {
      final data = jsonDecode(response.body);
      return UserModel.fromJson(data);
    } else {
      throw Exception('فشل تسجيل الدخول: ${response.statusCode}');
    }
  }

  Future<UserModel> register(String email, String password, String name) async {
    final url = Uri.parse('${ApiConstants.apiBase}${ApiConstants.register}');
    
    final response = await http.post(
      url,
      headers: {'Content-Type': 'application/json'},
      body: jsonEncode({
        'email': email,
        'password': password,
        'name': name,
      }),
    ).timeout(ApiConstants.connectionTimeout);

    if (response.statusCode == 201 || response.statusCode == 200) {
      final data = jsonDecode(response.body);
      return UserModel.fromJson(data);
    } else {
      throw Exception('فشل التسجيل: ${response.statusCode}');
    }
  }
}
