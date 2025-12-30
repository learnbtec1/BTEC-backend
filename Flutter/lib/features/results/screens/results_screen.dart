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