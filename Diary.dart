import 'package:flutter/material.dart';
import 'package:flutter_secure_storage/flutter_secure_storage.dart';
import 'dart:convert';
import 'dart:io';
import 'package:file_picker/file_picker.dart';
import 'package:path_provider/path_provider.dart';

void main() {
  runApp(EncryptedDiaryApp());
}

class EncryptedDiaryApp extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      debugShowCheckedModeBanner: false,
      theme: ThemeData(
        fontFamily: 'CursiveFont',
        brightness: Brightness.dark,
      ),
      home: DiaryLockScreen(),
    );
  }
}

class DiaryLockScreen extends StatefulWidget {
  @override
  _DiaryLockScreenState createState() => _DiaryLockScreenState();
}

class _DiaryLockScreenState extends State<DiaryLockScreen> {
  final TextEditingController _passwordController = TextEditingController();
  final FlutterSecureStorage storage = FlutterSecureStorage();
  String storedPassword = "1234";
  String emergencyPhrase = "petname";

  void _authenticate() async {
    if (_passwordController.text == storedPassword) {
      Navigator.push(
        context,
        MaterialPageRoute(builder: (context) => DiaryHomePage()),
      );
    } else if (_passwordController.text == emergencyPhrase) {
      Navigator.push(
        context,
        MaterialPageRoute(builder: (context) => DecoyDiaryPage()),
      );
    } else {
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(content: Text('Incorrect Password')),
      );
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: Center(
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            TextField(
              controller: _passwordController,
              obscureText: true,
              decoration: InputDecoration(labelText: 'Enter Password'),
            ),
            ElevatedButton(
              onPressed: _authenticate,
              child: Text('Unlock Diary'),
            ),
          ],
        ),
      ),
    );
  }
}

class DiaryHomePage extends StatefulWidget {
  @override
  _DiaryHomePageState createState() => _DiaryHomePageState();
}

class _DiaryHomePageState extends State<DiaryHomePage> {
  final FlutterSecureStorage storage = FlutterSecureStorage();
  final PageController _pageController = PageController();
  List<String> _entries = [];
  List<File> _attachments = [];

  @override
  void initState() {
    super.initState();
    _loadEntries();
  }

  Future<void> _loadEntries() async {
    String? encryptedData = await storage.read(key: 'diary_entries');
    if (encryptedData != null) {
      setState(() {
        _entries = List<String>.from(json.decode(encryptedData));
      });
    }
  }

  Future<void> _addEntry(String entry) async {
    setState(() {
      _entries.add(entry);
    });
    await storage.write(key: 'diary_entries', value: json.encode(_entries));
  }

  Future<void> _pickFile() async {
    FilePickerResult? result = await FilePicker.platform.pickFiles();
    if (result != null) {
      setState(() {
        _attachments.add(File(result.files.single.path!));
      });
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: Text('Encrypted Diary')),
      body: Column(
        children: [
          Expanded(
            child: PageView.builder(
              controller: _pageController,
              itemCount: _entries.length,
              itemBuilder: (context, index) {
                return Container(
                  decoration: BoxDecoration(
                    image: DecorationImage(
                      image: AssetImage('assets/vintage_texture.png'),
                      fit: BoxFit.cover,
                    ),
                  ),
                  child: Center(
                    child: Text(
                      _entries[index],
                      style: TextStyle(fontSize: 20, fontStyle: FontStyle.italic),
                    ),
                  ),
                );
              },
            ),
          ),
          Padding(
            padding: const EdgeInsets.all(8.0),
            child: Row(
              mainAxisAlignment: MainAxisAlignment.spaceEvenly,
              children: [
                ElevatedButton(
                  onPressed: _pickFile,
                  child: Text('Attach File'),
                ),
                ElevatedButton(
                  onPressed: () {
                    showDialog(
                      context: context,
                      builder: (context) {
                        TextEditingController _entryController = TextEditingController();
                        return AlertDialog(
                          title: Text('New Entry'),
                          content: TextField(controller: _entryController),
                          actions: [
                            ElevatedButton(
                              onPressed: () {
                                _addEntry(_entryController.text);
                                Navigator.pop(context);
                              },
                              child: Text('Save'),
                            ),
                          ],
                        );
                      },
                    );
                  },
                  child: Text('New Entry'),
                ),
              ],
            ),
          ),
        ],
      ),
    );
  }
}

class DecoyDiaryPage extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: Text('Decoy Diary')),
      body: Center(
        child: Text(
          'This is a fake diary for emergencies.',
          style: TextStyle(fontSize: 18, fontStyle: FontStyle.italic),
        ),
      ),
    );
  }
}
