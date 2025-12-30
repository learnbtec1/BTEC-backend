class UserModel {
  final String id;
  final String email;
  final String name;
  final String? token;

  UserModel({
    required this.id,
    required this.email,
    required this.name,
    this.token,
  });

  factory UserModel.fromJson(Map<String, dynamic> json) {
    return UserModel(
      id: json['id'] ?? '',
      email: json['email'] ?? '',
      name: json['name'] ?? json['full_name'] ?? '',
      token: json['token'] ?? json['access_token'],
    );
  }

  Map<String, dynamic> toJson() {
    return {
      'id': id,
      'email': email,
      'name': name,
      'token': token,
    };
  }
}
