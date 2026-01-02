import 'package:flutter/material.dart';

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
      _result = 'التقييم: 85%\nالتشابه: 92%\nالحالة: ممتاز';
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