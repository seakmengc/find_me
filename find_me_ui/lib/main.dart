import 'dart:async';
import 'dart:convert';

import 'package:flutter/material.dart';
import 'package:flutter_parsed_text/flutter_parsed_text.dart';
import 'package:http/http.dart' as http;
import 'package:url_launcher/url_launcher.dart';

import 'centered_view.dart';

void main() => runApp(MyApp());

class MyApp extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      debugShowCheckedModeBanner: false,
      title: 'Find Me UI',
      theme: ThemeData(
        primarySwatch: Colors.blue,
        textTheme: Theme.of(context).textTheme.apply(fontFamily: 'Open Sans'),
      ),
      home: HomeView(),
    );
  }
}

class HomeView extends StatefulWidget {
  const HomeView({Key? key}) : super(key: key);

  @override
  _HomeViewState createState() => _HomeViewState();
}

class _HomeViewState extends State<HomeView> {
  Timer? _debounce;
  final _controller = TextEditingController();
  bool _isBusy = false;

  Map _queryResults = {};

  onSearchChanged() {
    if (_debounce?.isActive ?? false) _debounce?.cancel();
    _debounce = Timer(const Duration(milliseconds: 250), () {
      _search();
    });
  }

  _search() async {
    try {
      setState(() {
        _isBusy = true;
      });
      final res = await http.get(
        Uri.parse(
            'http://127.0.0.1:5000/search?query=${_controller.text.toLowerCase()}'),
      );
      _queryResults = jsonDecode(res.body);
    } catch (e) {
      print(e);
    }
    setState(() {
      _isBusy = false;
    });
  }

  @override
  void dispose() {
    _controller.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    final List results = _queryResults['results'] ?? [];
    final time = _queryResults['time_to_search_in_milliseconds'] ?? [];

    return Scaffold(
      backgroundColor: Colors.white,
      appBar: AppBar(
        title: Text('CS 382 Portfolio - Find Me'),
      ),
      body: CenteredView(
        child: ListView(
          children: [
            ClipRRect(
              borderRadius: BorderRadius.circular(20),
              child: TextField(
                controller: _controller,
                onChanged: (val) => onSearchChanged(),
                onSubmitted: (val) => _search(),
                decoration: InputDecoration(
                  contentPadding: const EdgeInsets.symmetric(
                    horizontal: 20,
                    vertical: 15,
                  ),
                  fillColor: Colors.grey[250],
                  filled: true,
                  border: InputBorder.none,
                ),
              ),
            ),
            const SizedBox(height: 15),
            Row(
              mainAxisAlignment: MainAxisAlignment.end,
              children: [
                ElevatedButton(
                  onPressed: _search,
                  child: Text('Search'),
                ),
              ],
            ),
            if (_isBusy) LinearProgressIndicator(),
            if (!_isBusy) ...[
              if (results.isNotEmpty) ...[
                Text(
                  'Found ${results.length} result${results.length > 1 ? 's' : ''} ($time)',
                  style: TextStyle(
                    fontSize: 20,
                    fontWeight: FontWeight.w500,
                    color: Colors.grey[700],
                  ),
                ),
                const SizedBox(height: 10),
                ...results.map(
                  (e) => Padding(
                    padding: const EdgeInsets.symmetric(vertical: 5),
                    child: _Item(query: _controller.text, item: e),
                  ),
                ),
              ] else
                Text(
                  'No Result Found',
                  style: TextStyle(
                    fontSize: 20,
                    fontWeight: FontWeight.w500,
                    color: Colors.grey[700],
                  ),
                ),
            ],
          ],
        ),
      ),
    );
  }
}

class _Item extends StatelessWidget {
  final String query;
  final Map item;
  const _Item({Key? key, required this.item, required this.query})
      : super(key: key);

  RegExp get _pattern => RegExp(query.toLowerCase(), caseSensitive: false);

  Widget _textRow(String start, String? end, {bool isLink = false}) {
    // Iterable matches1 = pattern.allMatches(start);
    // Iterable matches2 = pattern.allMatches(end ?? '');
    // print(matches1.length);
    // print(matches2.length);

    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        Text(
          start,
          style: TextStyle(
            decoration: TextDecoration.underline,
            color: Colors.grey[800],
            fontWeight: FontWeight.w500,
          ),
        ),
        const SizedBox(height: 5),
        GestureDetector(
          onTap: () {
            if (isLink && end != null) launch(end.toString());
          },
          child: ParsedText(
            text: end ?? '',
            parse: [
              MatchText(
                pattern: _pattern.pattern,
                style: TextStyle(
                  fontWeight: FontWeight.w600,
                  color: Colors.blue,
                ),
                onTap: (url) async {},
              ),
            ],
          ),
          // Text(
          //   end ?? '',
          //   style: TextStyle(
          //     color: isLink ? Colors.blue : null,
          //   ),
          // ),
        ),
      ],
    );
  }

  @override
  Widget build(BuildContext context) {
    return Card(
      child: Container(
        padding: const EdgeInsets.all(15),
        decoration: BoxDecoration(
          color: Colors.grey[50],
          borderRadius: BorderRadius.circular(10),
        ),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            _textRow('Title', item['title']),
            const SizedBox(height: 10),
            _textRow('Description', item['description']),
            const SizedBox(height: 10),
            _textRow('Score', item['score'].toString()),
            const SizedBox(height: 10),
            _textRow('Url', item['url'], isLink: true),
          ],
        ),
      ),
    );
  }
}
