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
    // if (_debounce?.isActive ?? false) _debounce?.cancel();
    // _debounce = Timer(const Duration(milliseconds: 250), () {
    //   _search();
    // });
  }

  _search() async {
    if (_controller.text.toLowerCase().isEmpty) {
      return;
    }

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
                autofocus: true,
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

  List<RegExp> get _patterns => query
      .toLowerCase()
      .split(' ')
      .map((e) => RegExp("\\b($e)\\b", caseSensitive: false))
      .toList();

  @override
  Widget build(BuildContext context) {
    return InkWell(
      hoverColor: Colors.blueGrey,
      onHover: (bool boolean) {},
      child: Card(
        elevation: 7.0,
        child: Container(
          padding: const EdgeInsets.all(15),
          decoration: BoxDecoration(
            color: Colors.grey[50],
            borderRadius: BorderRadius.circular(10),
          ),
          child: ListTile(
            trailing: CircleAvatar(
              backgroundColor: Colors.blue,
              child: Text(
                item['score'].toStringAsFixed(2),
                style: TextStyle(
                  color: Colors.white,
                ),
              ),
            ),
            title: TextRow(
              patterns: _patterns,
              text: item['title'],
              style: TextStyle(
                fontSize: 24,
                color: Colors.blue,
                decoration: TextDecoration.underline,
              ),
              url: item['url'],
            ),
            subtitle: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                InkWell(
                  onHover: (bool boolean) {},
                  onTap: () {
                    launch(item['url']);
                  },
                  child: Text(
                    item['url'],
                    style: TextStyle(
                      decoration: TextDecoration.underline,
                      color: Colors.green,
                    ),
                  ),
                ),
                const SizedBox(height: 7),
                TextRow(
                  patterns: _patterns,
                  text: item['description'],
                ),
                const SizedBox(height: 7),
                Text(item['scores'].toString()),
              ],
            ),
          ),
        ),
      ),
    );
  }
}

class TextRow extends StatelessWidget {
  final String text;
  final TextStyle? style;
  final String? url;

  const TextRow({
    required List<RegExp> patterns,
    required this.text,
    this.style,
    this.url,
  }) : _patterns = patterns;

  final List<RegExp> _patterns;

  @override
  Widget build(BuildContext context) {
    return Padding(
      padding: const EdgeInsets.only(bottom: 8.0),
      child: InkWell(
        onTap: url == null
            ? null
            : () {
                launch(url!);
              },
        child: ParsedText(
          text: text,
          style: style,
          parse: _patterns.map((RegExp pattern) {
            return MatchText(
              pattern: pattern.pattern,
              style: TextStyle(
                fontWeight: FontWeight.w900,
                // color: Colors.blue,
              ),
              onTap: (url) async {},
            );
          }).toList(),
        ),
      ),
    );
  }
}
