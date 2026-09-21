// Minimal Persian-only "IT support status" screen shown on the normal
// end-user desktop main window (DesktopType.main). It intentionally does
// NOT expose any settings/password/network/account UI: it only shows the
// self ID, connection status, and a copy-id button, for employees to read
// out to IT support.
//
// This screen reuses the existing ServerModel (gFFI.serverModel) for the
// self ID (`serverId.text`, kept fresh by DesktopHomePage's periodic
// `fetchID()` calls) and connection status (`connectStatus`, kept fresh by
// ServerModel's own internal timer). No new FFI/backend calls are added.

import 'package:flutter/material.dart';
import 'package:flutter/services.dart';
import 'package:provider/provider.dart';

import '../../common.dart' show showToast, gFFI;
import '../../common/widgets/login.dart' show loginDialog;
import '../../models/server_model.dart';

/// Maps ASCII digits to Persian (Farsi) digits.
const Map<String, String> _asciiToPersianDigit = {
  '0': '۰',
  '1': '۱',
  '2': '۲',
  '3': '۳',
  '4': '۴',
  '5': '۵',
  '6': '۶',
  '7': '۷',
  '8': '۸',
  '9': '۹',
};

/// Converts ASCII digits in [input] to Persian digits. Non-digit
/// characters are left untouched. Never throws.
String toPersianDigits(String input) {
  final buffer = StringBuffer();
  for (final ch in input.split('')) {
    buffer.write(_asciiToPersianDigit[ch] ?? ch);
  }
  return buffer.toString();
}

/// Formats [id] for display: Persian digits, grouped in 3s from the left
/// (e.g. "907214583" -> "۹۰۷ ۲۱۴ ۵۸۳"). If [id] is empty or not purely
/// numeric (or shorter than 3 digits), it still returns a safe,
/// Persian-digit-substituted string without grouping or throwing.
String formatIdForDisplay(String id) {
  if (id.isEmpty) return '';
  final isNumeric = RegExp(r'^[0-9]+$').hasMatch(id);
  if (!isNumeric) {
    return toPersianDigits(id);
  }
  final groups = <String>[];
  for (int i = 0; i < id.length; i += 3) {
    final end = (i + 3 < id.length) ? i + 3 : id.length;
    groups.add(id.substring(i, end));
  }
  return toPersianDigits(groups.join(' '));
}

/// The minimal Persian, RTL "IT support status" screen for ordinary
/// employees. Shown as the entire body of the main desktop window.
class DesktopStatusPage extends StatelessWidget {
  const DesktopStatusPage({Key? key}) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return Directionality(
      textDirection: TextDirection.rtl,
      child: ChangeNotifierProvider.value(
        value: gFFI.serverModel,
        child: Consumer<ServerModel>(
          builder: (context, model, _) => _StatusBody(model: model),
        ),
      ),
    );
  }
}

class _StatusBody extends StatelessWidget {
  final ServerModel model;

  const _StatusBody({Key? key, required this.model}) : super(key: key);

  // ServerModel.connectStatus: 0 = connecting, -1 = not ready, 1 = ready.
  bool get _isConnected => model.connectStatus == 1;

  @override
  Widget build(BuildContext context) {
    final rawId = model.serverId.text;
    final displayId = formatIdForDisplay(rawId);
    return Material(
      color: Theme.of(context).scaffoldBackgroundColor,
      child: Center(
        child: SingleChildScrollView(
          padding: const EdgeInsets.symmetric(horizontal: 32, vertical: 24),
          child: ConstrainedBox(
            constraints: const BoxConstraints(maxWidth: 420),
            child: Column(
              mainAxisSize: MainAxisSize.min,
              crossAxisAlignment: CrossAxisAlignment.center,
              children: [
                Image.asset(
                  'assets/logo.png',
                  height: 64,
                  errorBuilder: (_, __, ___) => const SizedBox.shrink(),
                ),
                const SizedBox(height: 20),
                // Low-visibility admin-login reveal: a long-press on the
                // title opens the existing account login dialog
                // (common/widgets/login.dart -> loginDialog()). This is
                // deliberately not a visible button/icon so ordinary
                // employees never see a login affordance; only someone who
                // already knows to long-press the title (an admin) finds
                // it. No new auth is implemented here — loginDialog()
                // reuses the existing username/password + OIDC login flow
                // and stores the session in the existing local-option
                // token storage (access_token / user_info) exactly the
                // same way the rest of the app already does.
                GestureDetector(
                  onLongPress: () {
                    loginDialog();
                  },
                  child: Text(
                    'پشتیبانی فناوری اطلاعات',
                    textAlign: TextAlign.right,
                    style: Theme.of(context)
                        .textTheme
                        .headlineSmall
                        ?.copyWith(fontWeight: FontWeight.bold),
                  ),
                ),
                const SizedBox(height: 28),
                Align(
                  alignment: Alignment.centerRight,
                  child: Text(
                    'شناسه سیستم شما:',
                    textAlign: TextAlign.right,
                    style: Theme.of(context).textTheme.titleMedium,
                  ),
                ),
                const SizedBox(height: 8),
                Container(
                  width: double.infinity,
                  padding:
                      const EdgeInsets.symmetric(vertical: 16, horizontal: 12),
                  decoration: BoxDecoration(
                    color: Theme.of(context).colorScheme.surfaceVariant,
                    borderRadius: BorderRadius.circular(8),
                  ),
                  child: Text(
                    displayId.isEmpty ? '—' : displayId,
                    textAlign: TextAlign.center,
                    style: const TextStyle(
                      fontSize: 30,
                      fontWeight: FontWeight.bold,
                      letterSpacing: 2,
                    ),
                  ),
                ),
                const SizedBox(height: 16),
                Text(
                  'این شناسه را هنگام ثبت درخواست پشتیبانی برای واحد فناوری اطلاعات ارسال کنید.',
                  textAlign: TextAlign.right,
                  style: Theme.of(context).textTheme.bodyMedium,
                ),
                const SizedBox(height: 24),
                Row(
                  mainAxisAlignment: MainAxisAlignment.center,
                  children: [
                    Container(
                      width: 12,
                      height: 12,
                      decoration: BoxDecoration(
                        shape: BoxShape.circle,
                        color: _isConnected ? Colors.green : Colors.red,
                      ),
                    ),
                    const SizedBox(width: 8),
                    Text(
                      _isConnected
                          ? 'متصل'
                          : (model.connectStatus == 0
                              ? 'درحال اتصال...'
                              : 'قطع'),
                      style: Theme.of(context).textTheme.bodyLarge,
                    ),
                  ],
                ),
                const SizedBox(height: 28),
                ElevatedButton(
                  onPressed: rawId.isEmpty
                      ? null
                      : () {
                          Clipboard.setData(ClipboardData(text: rawId));
                          showToast('شناسه کپی شد');
                        },
                  child: const Padding(
                    padding:
                        EdgeInsets.symmetric(horizontal: 24, vertical: 10),
                    child: Text('کپی شناسه', style: TextStyle(fontSize: 16)),
                  ),
                ),
              ],
            ),
          ),
        ),
      ),
    );
  }
}
