#!/usr/bin/env python3
"""
Script to generate complete Flutter app structure for BTEC Smart Platform
"""
from pathlib import Path

BASE_DIR = Path("Flutter/lib")

# File templates
FILES = {
    "core/constants/app_constants.dart": """
import 'package:flutter/material.dart';

class AppConstants {
  static const String appName = 'BTEC Smart Platform';
  static const Color primaryColor = Color(0xFF2196F3);
  static const Color secondaryColor = Color(0xFF03DAC6);
  static const double padding = 16.0;
}
""",
    
    "core/network/api_client.dart": """
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
""",

    "main.dart": """
import 'package:flutter/material.dart';
import 'features/auth/screens/login_screen.dart';
import 'core/constants/app_constants.dart';

void main() {
  runApp(const BTECApp());
}

class BTECApp extends StatelessWidget {
  const BTECApp({Key? key}) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: AppConstants.appName,
      debugShowCheckedModeBanner: false,
      theme: ThemeData(
        primaryColor: AppConstants.primaryColor,
        fontFamily: 'Cairo',
        useMaterial3: true,
        colorScheme: ColorScheme.fromSeed(
          seedColor: AppConstants.primaryColor,
        ),
      ),
      home: const LoginScreen(),
    );
  }
}
""",

    "features/auth/screens/login_screen.dart": """
import 'package:flutter/material.dart';
import '../../dashboard/screens/dashboard_screen.dart';

class LoginScreen extends StatefulWidget {
  const LoginScreen({Key? key}) : super(key: key);

  @override
  State<LoginScreen> createState() => _LoginScreenState();
}

class _LoginScreenState extends State<LoginScreen> {
  final _emailController = TextEditingController();
  final _passwordController = TextEditingController();
  bool _isLoading = false;

  Future<void> _login() async {
    setState(() => _isLoading = true);
    
    await Future.delayed(const Duration(seconds: 1));
    
    if (mounted) {
      Navigator.pushReplacement(
        context,
        MaterialPageRoute(builder: (_) => const DashboardScreen()),
      );
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: Container(
        decoration: BoxDecoration(
          gradient: LinearGradient(
            begin: Alignment.topCenter,
            end: Alignment.bottomCenter,
            colors: [Colors.blue.shade700, Colors.blue.shade400],
          ),
        ),
        child: SafeArea(
          child: Center(
            child: SingleChildScrollView(
              padding: const EdgeInsets.all(24.0),
              child: Card(
                elevation: 8,
                shape: RoundedRectangleBorder(
                  borderRadius: BorderRadius.circular(16),
                ),
                child: Padding(
                  padding: const EdgeInsets.all(24.0),
                  child: Column(
                    mainAxisSize: MainAxisSize.min,
                    children: [
                      const Icon(Icons.school, size: 80, color: Colors.blue),
                      const SizedBox(height: 16),
                      const Text(
                        'BTEC Smart Platform',
                        style: TextStyle(fontSize: 24, fontWeight: FontWeight.bold),
                      ),
                      const SizedBox(height: 32),
                      TextField(
                        controller: _emailController,
                        decoration: const InputDecoration(
                          labelText: 'البريد الإلكتروني',
                          prefixIcon: Icon(Icons.email),
                          border: OutlineInputBorder(),
                        ),
                      ),
                      const SizedBox(height: 16),
                      TextField(
                        controller: _passwordController,
                        obscureText: true,
                        decoration: const InputDecoration(
                          labelText: 'كلمة المرور',
                          prefixIcon: Icon(Icons.lock),
                          border: OutlineInputBorder(),
                        ),
                      ),
                      const SizedBox(height: 24),
                      SizedBox(
                        width: double.infinity,
                        height: 50,
                        child: ElevatedButton(
                          onPressed: _isLoading ? null : _login,
                          child: _isLoading
                              ? const CircularProgressIndicator(color: Colors.white)
                              : const Text('تسجيل الدخول', style: TextStyle(fontSize: 18)),
                        ),
                      ),
                    ],
                  ),
                ),
              ),
            ),
          ),
        ),
      ),
    );
  }
}
""",

    "features/dashboard/screens/dashboard_screen.dart": """
import 'package:flutter/material.dart';
import '../../assessment/screens/assessment_screen.dart';
import '../../results/screens/results_screen.dart';
import '../../settings/screens/settings_screen.dart';

class DashboardScreen extends StatefulWidget {
  const DashboardScreen({Key? key}) : super(key: key);

  @override
  State<DashboardScreen> createState() => _DashboardScreenState();
}

class _DashboardScreenState extends State<DashboardScreen> {
  int _selectedIndex = 0;

  final List<Widget> _screens = [
    const DashboardHomeScreen(),
    const AssessmentScreen(),
    const ResultsScreen(),
    const SettingsScreen(),
  ];

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: _screens[_selectedIndex],
      bottomNavigationBar: NavigationBar(
        selectedIndex: _selectedIndex,
        onDestinationSelected: (index) {
          setState(() => _selectedIndex = index);
        },
        destinations: const [
          NavigationDestination(icon: Icon(Icons.home), label: 'الرئيسية'),
          NavigationDestination(icon: Icon(Icons.assessment), label: 'التقييم'),
          NavigationDestination(icon: Icon(Icons.analytics), label: 'النتائج'),
          NavigationDestination(icon: Icon(Icons.settings), label: 'الإعدادات'),
        ],
      ),
    );
  }
}

class DashboardHomeScreen extends StatelessWidget {
  const DashboardHomeScreen({Key? key}) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('لوحة التحكم'),
        centerTitle: true,
      ),
      body: Padding(
        padding: const EdgeInsets.all(16.0),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            const Text(
              'مرحباً بك في منصة BTEC',
              style: TextStyle(fontSize: 24, fontWeight: FontWeight.bold),
            ),
            const SizedBox(height: 24),
            Expanded(
              child: GridView.count(
                crossAxisCount: 2,
                crossAxisSpacing: 16,
                mainAxisSpacing: 16,
                children: [
                  _buildDashboardCard(
                    'التقييم النصي',
                    Icons.text_fields,
                    Colors.blue,
                  ),
                  _buildDashboardCard(
                    'التقييم الصوتي',
                    Icons.mic,
                    Colors.green,
                  ),
                  _buildDashboardCard(
                    'النتائج',
                    Icons.analytics,
                    Colors.orange,
                  ),
                  _buildDashboardCard(
                    'الإعدادات',
                    Icons.settings,
                    Colors.purple,
                  ),
                ],
              ),
            ),
          ],
        ),
      ),
    );
  }

  Widget _buildDashboardCard(String title, IconData icon, Color color) {
    return Card(
      elevation: 4,
      shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(16)),
      child: InkWell(
        onTap: () {},
        borderRadius: BorderRadius.circular(16),
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            Icon(icon, size: 48, color: color),
            const SizedBox(height: 12),
            Text(
              title,
              style: const TextStyle(fontSize: 16, fontWeight: FontWeight.bold),
              textAlign: TextAlign.center,
            ),
          ],
        ),
      ),
    );
  }
}
""",

    "features/assessment/screens/assessment_screen.dart": """
import 'package:flutter/material.dart';
import 'dart:io';

class AssessmentScreen extends StatefulWidget {
  const AssessmentScreen({Key? key}) : super(key: key);

  @override
  State<AssessmentScreen> createState() => _AssessmentScreenState();
}

class _AssessmentScreenState extends State<AssessmentScreen> {
  final _textController = TextEditingController();
  bool _isLoading = false;
  String _result = '';

  Future<void> _evaluate() async {
    setState(() {
      _isLoading = true;
      _result = '';
    });

    await Future.delayed(const Duration(seconds: 2));

    setState(() {
      _isLoading = false;
      _result = 'التقييم: 85%\\nالتشابه: 92%\\nالحالة: ممتاز';
    });
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('تقييم الإجابة'),
        centerTitle: true,
      ),
      body: SingleChildScrollView(
        padding: const EdgeInsets.all(16.0),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.stretch,
          children: [
            const Text(
              'أدخل إجابتك للتقييم',
              style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold),
            ),
            const SizedBox(height: 16),
            TextField(
              controller: _textController,
              maxLines: 10,
              decoration: const InputDecoration(
                hintText: 'اكتب إجابتك هنا...',
                border: OutlineInputBorder(),
              ),
            ),
            const SizedBox(height: 16),
            ElevatedButton.icon(
              onPressed: _isLoading ? null : _evaluate,
              icon: const Icon(Icons.check_circle),
              label: _isLoading
                  ? const Text('جاري التقييم...')
                  : const Text('تقييم الإجابة'),
              style: ElevatedButton.styleFrom(
                padding: const EdgeInsets.all(16),
              ),
            ),
            const SizedBox(height: 24),
            if (_result.isNotEmpty)
              Card(
                color: Colors.green.shade50,
                child: Padding(
                  padding: const EdgeInsets.all(16.0),
                  child: Column(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: [
                      const Text(
                        'نتيجة التقييم',
                        style: TextStyle(
                          fontSize: 18,
                          fontWeight: FontWeight.bold,
                        ),
                      ),
                      const SizedBox(height: 12),
                      Text(_result, style: const TextStyle(fontSize: 16)),
                    ],
                  ),
                ),
              ),
          ],
        ),
      ),
    );
  }
}
""",

    "features/results/screens/results_screen.dart": """
import 'package:flutter/material.dart';

class ResultsScreen extends StatelessWidget {
  const ResultsScreen({Key? key}) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('النتائج'),
        centerTitle: true,
      ),
      body: ListView.builder(
        padding: const EdgeInsets.all(16),
        itemCount: 5,
        itemBuilder: (context, index) {
          return Card(
            margin: const EdgeInsets.only(bottom: 12),
            child: ListTile(
              leading: CircleAvatar(
                backgroundColor: Colors.blue,
                child: Text('\${index + 1}'),
              ),
              title: Text('تقييم \${index + 1}'),
              subtitle: Text('التاريخ: 2024-01-\${15 + index}'),
              trailing: Chip(
                label: Text('\${85 + index}%'),
                backgroundColor: Colors.green.shade100,
              ),
              onTap: () {
                // Show details
              },
            ),
          );
        },
      ),
    );
  }
}
""",

    "features/settings/screens/settings_screen.dart": """
import 'package:flutter/material.dart';

class SettingsScreen extends StatelessWidget {
  const SettingsScreen({Key? key}) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('الإعدادات'),
        centerTitle: true,
      ),
      body: ListView(
        children: [
          ListTile(
            leading: const Icon(Icons.person),
            title: const Text('الملف الشخصي'),
            onTap: () {},
          ),
          ListTile(
            leading: const Icon(Icons.notifications),
            title: const Text('الإشعارات'),
            trailing: Switch(value: true, onChanged: (val) {}),
          ),
          ListTile(
            leading: const Icon(Icons.language),
            title: const Text('اللغة'),
            subtitle: const Text('العربية'),
            onTap: () {},
          ),
          const Divider(),
          ListTile(
            leading: const Icon(Icons.info),
            title: const Text('حول التطبيق'),
            onTap: () {},
          ),
          ListTile(
            leading: const Icon(Icons.logout, color: Colors.red),
            title: const Text('تسجيل الخروج', style: TextStyle(color: Colors.red)),
            onTap: () {},
          ),
        ],
      ),
    );
  }
}
""",
}

def generate_files():
    """Generate all Flutter files"""
    for file_path, content in FILES.items():
        full_path = BASE_DIR / file_path
        full_path.parent.mkdir(parents=True, exist_ok=True)
        full_path.write_text(content.strip())
        print(f"✓ Created: {file_path}")

if __name__ == "__main__":
    generate_files()
    print("\n✅ Flutter app structure generated successfully!")
