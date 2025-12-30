class AssessmentModel {
  final String id;
  final String studentAnswer;
  final String modelAnswer;
  final double similarity;
  final double levenshteinRatio;
  final String status;
  final DateTime createdAt;

  AssessmentModel({
    required this.id,
    required this.studentAnswer,
    required this.modelAnswer,
    required this.similarity,
    required this.levenshteinRatio,
    required this.status,
    required this.createdAt,
  });

  factory AssessmentModel.fromJson(Map<String, dynamic> json) {
    return AssessmentModel(
      id: json['id'] ?? '',
      studentAnswer: json['student_answer'] ?? '',
      modelAnswer: json['model_answer'] ?? '',
      similarity: (json['similarity'] ?? 0.0).toDouble(),
      levenshteinRatio: (json['levenshtein_ratio'] ?? 0.0).toDouble(),
      status: json['status'] ?? 'pending',
      createdAt: json['created_at'] != null 
          ? DateTime.parse(json['created_at'])
          : DateTime.now(),
    );
  }

  Map<String, dynamic> toJson() {
    return {
      'id': id,
      'student_answer': studentAnswer,
      'model_answer': modelAnswer,
      'similarity': similarity,
      'levenshtein_ratio': levenshteinRatio,
      'status': status,
      'created_at': createdAt.toIso8601String(),
    };
  }
  
  double get scorePercentage => (similarity * 100).clamp(0, 100);
  
  String get grade {
    if (scorePercentage >= 90) return 'ممتاز';
    if (scorePercentage >= 80) return 'جيد جداً';
    if (scorePercentage >= 70) return 'جيد';
    if (scorePercentage >= 60) return 'مقبول';
    return 'ضعيف';
  }
}
