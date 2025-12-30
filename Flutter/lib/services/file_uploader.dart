import 'package:flutter/foundation.dart';
import 'package:http/http.dart' as http;
import 'dart:typed_data';

class FileUploader {
  final String baseUrl;

  FileUploader({String? baseUrl})
      : baseUrl = baseUrl ?? 
          const String.fromEnvironment('API_BASE_URL', defaultValue: 'http://localhost:8000');

  Future<Map<String, dynamic>> uploadFile({
    String? filePath,
    Uint8List? fileBytes,
    String? fileName,
  }) async {
    final url = Uri.parse('$baseUrl/api/v1/upload');
    var request = http.MultipartRequest('POST', url);

    if (kIsWeb) {
      if (fileBytes == null || fileName == null) {
        throw Exception('fileBytes and fileName are required for web');
      }
      request.files.add(http.MultipartFile.fromBytes(
        'file',
        fileBytes,
        filename: fileName,
      ));
    } else {
      if (filePath == null) {
        throw Exception('filePath is required for mobile');
      }
      request.files.add(await http.MultipartFile.fromPath('file', filePath));
    }

    var response = await request.send();
    var responseBody = await response.stream.bytesToString();

    return {
      'statusCode': response.statusCode,
      'body': responseBody,
    };
  }
}
